import os
from decouple import config
from pathlib import Path
from dj_database_url import parse as dburl
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "rest_framework",
    "corsheaders",
    "djoser",
    # myapp
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 追加
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Nippo.urls"

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

WSGI_APPLICATION = "Nippo.wsgi.application"

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = config("TRUSTED_ORIGINS").split(",")

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# ↓ 追加
default_dburl = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": config(
        "POSTGRES_DB", default=os.environ.get("POSTGRES_NAME", "your_database_name")
    ),
    "USER": config(
        "POSTGRES_NAME", default=os.environ.get("POSTGRES_USER", "your_default_user")
    ),
    "PASSWORD": config(
        "POSTGRES_PASSWORD",
        default=os.environ.get("POSTGRES_PASSWORD", "your_default_password"),
    ),
    "HOST": "db",
    "PORT": 5432,
}

DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    DATABASES = {"default": dburl(DATABASE_URL)}
else:
    DATABASES = {"default": default_dburl}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest Framework設定
REST_FRAMEWORK = {
    # 認証が必要
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # JWT認証
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "auth.authenticate.CustomJWTAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# JWT設定
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # cookie settings
    "AUTH_COOKIE": "accessToken",  # cookie name
    "AUTH_COOKIE_REFRESH": "refreshToken",  # Cookie name. Enables cookies if value is set.
    "AUTH_COOKIE_DOMAIN": None,  # specifies domain for which the cookie will be sent
    "AUTH_COOKIE_SECURE": True,  # restricts the transmission of the cookie to only occur over secure (HTTPS) connections.
    "AUTH_COOKIE_HTTP_ONLY": True,  # prevents client-side js from accessing the cookie
    "AUTH_COOKIE_PATH": "/",  # URL path where cookie will be sent
    "AUTH_COOKIE_SAMESITE": "Lax",  # specifies whether the cookie should be sent in cross site requests
}

# Djoser設定
DJOSER = {}
# ユーザーモデル
AUTH_USER_MODEL = "accounts.UserAccount"

# CSRFの設定
# これがないと403エラーを返してしまう
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
