import os
from pathlib import Path

import cloudinary
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["*"]


GOOGLE_RECAPTCHA_SITE_KEY = os.getenv("GOOGLE_RECAPTCHA_SITE_KEY")
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY")

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_USER"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# DATABASE CACHE CONFIGURATION
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "TIMEOUT": 600,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}


# SMTP AND EMAIL CONFIGURATION FOR MAILING
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_EURO_MILLION_MONDE = os.getenv("EMAIL_EURO_MILLION_MONDE")
RECEIVER_MAIL_MESSAGE = os.getenv("RECEIVER_MAIL_MESSAGE")
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
RECEIVER_MAIL = os.getenv("RECEIVER_MAIL")
HOSTED_BUTTON_ID = os.getenv("HOSTED_BUTTON_ID")
FROM_EMAIL = os.getenv("FROM_EMAIL")


# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
    }
}
