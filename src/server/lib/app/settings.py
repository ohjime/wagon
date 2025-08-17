from pathlib import Path
import os

os.environ["DJANGO_RUNSERVER_HIDE_WARNING"] = "true"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Generate new key for Production
SECRET_KEY = "django-insecure-u8#1l$95&vq3w2(ei^=ng+4tdid@by!s+&u&jlizx&xr&w&(gk"
# False in Production
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_browser_reload",
    "django.contrib.staticfiles",
    "django_vite",
    "django_tables2",
    "core",
    "dashboard",
]
# if DEBUG:
#     INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# if DEBUG:
#     MIDDLEWARE += [
#         # NOTE: The middleware should be listed after any that encode
#         # the response, such as Django’s GZipMiddleware. The middleware
#         # automatically inserts the required script tag on HTML responses
#         # before </body> when DEBUG is True.
#         "django_browser_reload.middleware.BrowserReloadMiddleware",
#     ]
ROOT_URLCONF = "app.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "app.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_ROOT = BASE_DIR / "assets"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "vite/static",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
    }
}
