from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "5432",
    }
}

AWS_STORAGE_BUCKET_NAME = "NOT_SET_AWS_STORAGE_BUCKET_NAME"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

if DEBUG:
    print("Dev Mode: Sending emails locally")
    EMAIL_HOST = "mailcatcher"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

SUPER_ADMIN_PASS = "cfb1234567q"
