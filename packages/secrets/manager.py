# secret_manager.py
# Usage:
# 1. Create a .env file in your project root with:
#       GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
#    (and any other env vars like GOOGLE_APPLICATION_CREDENTIALS).
# 2. Install python-dotenv: pip install python-dotenv
# 3. The script will auto-load variables from .env.
# 4. Call SecretManager.get_secret("SECRET_ID") to retrieve secrets.

import os
import logging
from dotenv import load_dotenv
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound, PermissionDenied, GoogleAPIError

# Load environment variables from .env
load_dotenv()

# Define secret IDs
DB_USER_SECRET = "db_username"
DB_PASSWORD_SECRET = "db_password"
DB_NAME_SECRET = "db_name"

class SecretManager:
    """
    Wrapper for Google Secret Manager to fetch secrets by name.

    Args:
        project_id (str, optional): GCP project ID. Defaults to env var GOOGLE_CLOUD_PROJECT.
    """

    def __init__(self, project_id: str = None):
        # Use provided project_id or fall back to environment variable
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Specify project_id or set GOOGLE_CLOUD_PROJECT environment variable.")

        # Initialize the Secret Manager client
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        """
        Retrieve the payload of the given secret.

        Args:
            secret_id (str): ID of the secret in Secret Manager.
            version_id (str, optional): Version of the secret. Defaults to "latest".

        Returns:
            str: The secret value as a decoded UTF-8 string.

        Raises:
            NotFound: If the secret or version does not exist.
            PermissionDenied: If access is denied.
            GoogleAPIError: For other API errors.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except NotFound:
            logging.error(f"Secret '{secret_id}' not found in project {self.project_id}.")
            raise
        except PermissionDenied:
            logging.error(f"Permission denied accessing secret '{secret_id}'.")
            raise
        except GoogleAPIError as e:
            logging.error(f"Error fetching secret '{secret_id}': {e}")
            raise

def get_secret(secret_id: str, default_value: str = None) -> str:
    """
    Retrieve a secret from Secret Manager.

    Args:
        secret_id (str): ID of the secret in Secret Manager.
        default_value (str, optional): Default value to return if secret retrieval fails.

    Returns:
        str: The secret value or the default value if retrieval fails.
    """
    try:
        secret_manager = SecretManager()
        return secret_manager.get_secret(secret_id)
    except Exception as e:
        logging.warning(f"Failed to retrieve secret '{secret_id}': {e}")
        return default_value if default_value is not None else f"[{secret_id}]"

def add_secret_version(secret_id: str, secret_value: str) -> str:
    """
    Add a new version of a secret to Secret Manager.

    Args:
        secret_id (str): ID of the secret in Secret Manager.
        secret_value (str): Value to store as the new secret version.

    Returns:
        str: The name of the new secret version.
    """
    try:
        secret_manager = SecretManager()
        project_id = secret_manager.project_id
        client = secret_manager.client

        # Create the parent resource
        parent = f"projects/{project_id}"

        # Create the secret if it doesn't exist
        try:
            secret_path = f"{parent}/secrets/{secret_id}"
            client.get_secret(request={"name": secret_path})
        except NotFound:
            # Secret doesn't exist, create it
            client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )

        # Add the secret version
        response = client.add_secret_version(
            request={
                "parent": f"{parent}/secrets/{secret_id}",
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )

        logging.info(f"Added secret version: {response.name}")
        return response.name
    except Exception as e:
        logging.error(f"Failed to add secret version for '{secret_id}': {e}")
        raise

if __name__ == "__main__":
    # Example usage
    # Optionally override project_id:
    # secret_manager = SecretManager(project_id="your-gcp-project-id")
    secret_manager = SecretManager()

    try:
        # Replace with your actual secret names
        db_user = secret_manager.get_secret(DB_USER_SECRET)
        db_password = secret_manager.get_secret(DB_PASSWORD_SECRET)
        print(f"DB_USER: {db_user}")  # Remove printing in production
        print(f"DB_PASSWORD: {db_password}")
    except Exception:
        logging.exception("Failed to retrieve secrets.")
