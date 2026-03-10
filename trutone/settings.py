"""
Django settings for trutone project.

This settings file:
- loads environment variables from a .env file (python-dotenv)
- uses env vars for secrets, DB, and email configuration
- provides safe defaults for local development (console email backend)
- includes production-oriented security toggles (enable via env)
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

# -----------------------------------------------------------------------------
# Basic / security
# -----------------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-please-change")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# ALLOWED_HOSTS: comma-separated in env, default to localhost for dev
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# When deploying to production, set DJANGO_DEBUG=False and configure these:
if not DEBUG:
    # Recommended production security settings (tune values for your environment)
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True") == "True"
    CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 31536000))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False") == "True"
else:
    # Development defaults
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# -----------------------------------------------------------------------------
# Media / uploads
# -----------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Upload limits (adjust as needed)
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get("FILE_UPLOAD_MAX_MEMORY_SIZE", 2621440))  # 2.5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get("DATA_UPLOAD_MAX_MEMORY_SIZE", 10485760))  # 10 MB

# -----------------------------------------------------------------------------
# Email configuration (console by default for dev)
# -----------------------------------------------------------------------------
# Supported env variables:
# EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL,
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"

# Accept either EMAIL_HOST_USER/EMAIL_HOST_PASSWORD or SENDGRID_USER/SENDGRID_API_KEY
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", os.environ.get("SENDGRID_USER", "apikey"))
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", os.environ.get("SENDGRID_API_KEY", ""))

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@localhost")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

# -----------------------------------------------------------------------------
# Application definition
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "trutone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "trutone.wsgi.application"

# -----------------------------------------------------------------------------
# Database (Postgres via env)
# -----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "trutone"),
        "USER": os.environ.get("POSTGRES_USER", "trutone"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", os.environ.get("POSTGRES_HOST", "db")),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Optional DATABASE_URL support (if you use dj-database-url)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    except Exception:
        # dj-database-url is optional; ignore if not installed
        pass

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static files (whitenoise)
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------------------------------------------------------------
# Default primary key field type
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# Logging (basic, prints errors to console)
# -----------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

# -----------------------------------------------------------------------------
# Additional production settings you may want to enable when DEBUG=False
# -----------------------------------------------------------------------------
# Example:
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# X_FRAME_OPTIONS = 'DENY'
# CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# -----------------------------------------------------------------------------
# Helpful dev-time defaults (do not rely on these in production)
# -----------------------------------------------------------------------------
if DEBUG:
    # Show SQL in dev if desired
    if os.environ.get("DJANGO_SHOW_SQL", "False") == "True":
        LOGGING["loggers"]["django.db.backends"] = {"handlers": ["console"], "level": "DEBUG"}

# -----------------------------------------------------------------------------
# End of settings
# -----------------------------------------------------------------------------
