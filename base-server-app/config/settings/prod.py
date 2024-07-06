import logging

from .base import *

logger = logging.getLogger("setting_warnings")

# LOGGING
LOGGING = {
    "version": 1,
    "loggers": {
        "setting_warnings": {"level": "WARNING"},
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TESTING = False

SECURE_SSL_REDIRECT = False  # handled by load balancer otherwise change
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # TODO: Set ALLOWED_HOSTS to include domain
ALLOWED_CIDR_NETS = ["10.0.0.0/16"]  # TODO: verify
CORS_ALLOWED_ORIGINS = [
    ""
]  # TODO: Set CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGIN_REGEXES

if all([host in ["", "*"] for host in ALLOWED_HOSTS]):
    logger.warning(
        'WARNING: The settings.ALLOWED_HOSTS should not be "" or "*" on production. '
    )

if all([origin in ["", "*"] for origin in CORS_ALLOWED_ORIGINS]):
    logger.warning(
        'WARNING: The settings.CORS_ALLOWED_ORIGINS should not be "" or "*" on production. '
    )


db_dict = get_database_dict()
DATABASES = {"default": db_dict}

AWS_STORAGE_BUCKET_NAME = "base-prod"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
