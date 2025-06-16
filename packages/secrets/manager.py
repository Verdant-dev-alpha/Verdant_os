# Secret management module
import os
import logging
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound, PermissionDenied, ResourceExhausted

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database secret names
DB_USER_SECRET = "db-user"
DB_PASSWORD_SECRET = "db-password"
DB_NAME_SECRET = "db-name"

def get_secret(secret_name, default=None):
    """Retrieve secret from Secret Manager.

    Args:
        secret_name: Name of the secret to retrieve
        default: Default value to return if secret cannot be retrieved

    Returns:
        The secret value as a string, or the default value if the secret cannot be retrieved
    """
    # Check if GOOGLE_CLOUD_PROJECT is set
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        logger.warning("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot access Secret Manager.")
        return default

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

        logger.info(f"Retrieving secret {secret_name} from project {project_id}")
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    except NotFound:
        logger.warning(f"Secret {secret_name} not found in project {project_id}")
        return default
    except PermissionDenied:
        logger.error(f"Permission denied accessing secret {secret_name}. Check IAM permissions.")
        return default
    except ResourceExhausted:
        logger.error(f"Resource quota exceeded when accessing secret {secret_name}")
        return default
    except Exception as e:
        logger.error(f"Unexpected error retrieving secret {secret_name}: {e}", exc_info=True)
        return default
