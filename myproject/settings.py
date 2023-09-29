from pathlib import Path
from decouple import config

# Define the base directory of the Django project.
# This is used for constructing absolute paths to various resources.
BASE_DIR = Path(__file__).resolve().parent.parent

# Fetch the secret key from environment or a .env file.
# This key is used for cryptographic signing in Django.
SECRET_KEY = config("SECRET_KEY")

# Fetch the DEBUG setting from environment or a .env file.
# It determines if the application is in debug mode (not recommended for production).
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# A list of IP addresses or hostnames which can be used to access the application.
# Should be updated for production to restrict access.
ALLOWED_HOSTS = []


# Application definition

# List of applications (both built-in and custom) that are enabled for this Django project.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "custom_messages",
    "friends",
    "group_chat",
    "rest_framework",
    "rest_framework.authtoken",
]

# List of middleware classes that process request and response globally.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The main URL configuration for the project.
ROOT_URLCONF = "myproject.urls"

# Configuration for Django's templating system.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI configuration for serving the Django application.
WSGI_APPLICATION = "myproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Here, PostgreSQL is used as the database with credentials fetched from environment or .env file.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DATABASE_NAME"),
        'USER': config("DATABASE_USER"),
        'PASSWORD': config("DATABASE_PASSWORD"),
        'HOST': config("DATABASE_HOST"),
        'PORT': config("DATABASE_PORT"),
    }
}

# Validators for user passwords.
# They ensure passwords adhere to certain security standards.

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Settings for internationalization and localization.
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Settings for static files (CSS, JS, images).
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Default type for auto-generated primary key fields.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Specifies a custom user model named "CustomUser" in the "users" app.
AUTH_USER_MODEL = "users.CustomUser"

# Configuration for Django Rest Framework (DRF).
# It specifies authentication, parsing, and permission settings for DRF.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'TOKEN_MODEL': 'users.ExpiringToken'
}

# Configuration for logging in Django.
# Currently, logs of level DEBUG are printed to the console for 'django' and 'users' modules.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
