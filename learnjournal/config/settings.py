import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Classroom defaults keep a fresh clone runnable. Production should always set
# these values through environment variables (covered by the Deployment deck).
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-learnjournal-classroom-only-change-in-production")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "journal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "journal.middleware.ResponseTimeMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # MaintenanceModeMiddleware needs request.user, so it comes after auth.
    "journal.middleware.MaintenanceModeMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "journal.context_processors.site_nav",
                "journal.context_processors.reader_preferences",
            ],
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# SQLite remains the zero-setup classroom default. Set DJANGO_DB_ENGINE=postgresql
# and the DJANGO_DB_* variables to exercise PostgreSQL/full-text search.
if os.getenv("DJANGO_DB_ENGINE", "sqlite") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DJANGO_DB_NAME", "learnjournal"),
            "USER": os.getenv("DJANGO_DB_USER", "learnjournal"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", ""),
            "HOST": os.getenv("DJANGO_DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "journal.User"
LOGIN_REDIRECT_URL = "journal:home"
LOGOUT_REDIRECT_URL = "journal:home"
LOGIN_URL = "login"

# Bootstrap uses `danger`; Django's default error message tag is `error`.
MESSAGE_TAGS = {40: "danger"}

# Django 6.1 introduces MAILERS and deprecates EMAIL_BACKEND plus the older
# EMAIL_* connection settings. Development uses the console backend so students
# can inspect password-reset and subscription messages without an SMTP service.
MAILERS = {
    "default": {
        "BACKEND": os.getenv(
            "DJANGO_MAILER_BACKEND",
            "django.core.mail.backends.console.EmailBackend",
        ),
        "OPTIONS": {},
    }
}
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "LearnJournal <no-reply@learnjournal.example>")

# Local memory is deliberately used for class. A multi-process production
# deployment should use a shared cache such as Redis.
CACHES = {
    "default": {
        "BACKEND": os.getenv("DJANGO_CACHE_BACKEND", "django.core.cache.backends.locmem.LocMemCache"),
        "LOCATION": os.getenv("DJANGO_CACHE_LOCATION", "learnjournal-locmem"),
    }
}

# Classroom switch used by MaintenanceModeMiddleware.
MAINTENANCE_MODE = os.getenv("DJANGO_MAINTENANCE_MODE", "0") == "1"

# Production-oriented cookie/header defaults become active automatically when
# DEBUG is disabled. The Deployment deck explains reverse-proxy HTTPS details.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
