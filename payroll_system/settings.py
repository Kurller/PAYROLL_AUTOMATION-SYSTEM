from pathlib import Path
from decouple import config
from datetime import timedelta


# =====================================
# Base directory
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================
# Security
# =====================================

SECRET_KEY = config("SECRET_KEY")

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)

PAYSTACK_SECRET_KEY = config(
    "PAYSTACK_SECRET_KEY"
)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost"
).split(",")


# =====================================
# Installed apps
# =====================================

INSTALLED_APPS = [

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
     "drf_yasg",
    # Local apps
    "accounts",
    "employees",
    "payroll",
    "payments",
    "logs",
]


# =====================================
# Middleware
# =====================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)
# =====================================
# URL configuration
# =====================================

ROOT_URLCONF = "payroll_system.urls"


# =====================================
# Templates
# =====================================

TEMPLATES = [
    {
        "BACKEND":
        "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ]
        }
    }
]


# =====================================
# WSGI
# =====================================

WSGI_APPLICATION = "payroll_system.wsgi.application"


# =====================================
# PostgreSQL
# =====================================

DATABASES = {

    "default": {

        "ENGINE":
        "django.db.backends.postgresql",

        "NAME":
        config("DB_NAME"),

        "USER":
        config("DB_USER"),

        "PASSWORD":
        config("DB_PASSWORD"),

        "HOST":
        config(
            "DB_HOST",
            default="localhost"
        ),

        "PORT":
        config(
            "DB_PORT",
            default=5432,
            cast=int
        ),
    }
}


# =====================================
# REST framework
# =====================================

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": [

        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ]
}


# =====================================
# JWT settings
# =====================================

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME":
    timedelta(hours=1),

    "REFRESH_TOKEN_LIFETIME":
    timedelta(days=7),

    "ROTATE_REFRESH_TOKENS":
    False,

    "BLACKLIST_AFTER_ROTATION":
    True,

    "AUTH_HEADER_TYPES":
    ("Bearer",),
}


# =====================================
# Password validation
# =====================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =====================================
# Internationalization
# =====================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =====================================
# Static files
# =====================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# =====================================
# CORS
# =====================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]


# =====================================
# Production security
# =====================================

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"


# =====================================
# Logging
# =====================================

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {

        "file": {

            "class":
            "logging.FileHandler",

            "filename":
            BASE_DIR / "payroll.log"
        }
    },

    "root": {

        "handlers": ["file"],

        "level": "INFO"
    }
}


# =====================================
# Default primary key
# =====================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"