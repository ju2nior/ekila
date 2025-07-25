import os
from pathlib import Path

import cloudinary
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["www.mnlvm.com", "https://mnlvm.com", "mnlvm.com"]

MEDIA_ROOT = "/home/tgmszbpv/website/media"
MEDIA_URL = "/media/"


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


GOOGLE_RECAPTCHA_SITE_KEY = os.getenv("GOOGLE_RECAPTCHA_SITE_KEY")
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY")

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_USER"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# CORS CONF
CACHE_MIDDLEWARE_SECONDS = 300
CORS_ALLOWED_ORIGINS = [
    "https://mnlvm.com",
    "https://mnlvm.vercel.app",
    "https://mnlv-radio.netlify.app",
    "http://localhost:3000",
    "http://localhost:8080",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://mnlvm.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://mnlv-radio.netlify.app",
    "https://mnlvm.vercel.app",
]

# DATABASE CACHE CONFIGURATION
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "TIMEOUT": 600,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}


# JOURNALISATION DES LOGS
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/home/tgmszbpv/website/debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# https settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# sessions config
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 259200
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = "None"

# hsts settings
SECURE_HSTS_SECONDS = 31536000  # 1 YEAR
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


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

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}
