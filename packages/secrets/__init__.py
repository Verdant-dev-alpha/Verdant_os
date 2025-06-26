# Initialize the secrets package
from .manager import get_secret, add_secret_version, DB_USER_SECRET, DB_PASSWORD_SECRET, DB_NAME_SECRET

__all__ = ["get_secret", "add_secret_version", "DB_USER_SECRET", "DB_PASSWORD_SECRET", "DB_NAME_SECRET"]
