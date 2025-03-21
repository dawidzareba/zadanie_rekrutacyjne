from pathlib import Path

import environ

env = environ.Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
OTHER_APPS = [
    "rest_framework",
    "constance",
]
MY_APPS = ["apps.url_shortener"]

INSTALLED_APPS = DJANGO_APPS + OTHER_APPS + MY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

POSTGRES_DB = env.str("DB_NAME", default="zadanie")
POSTGRES_HOST = env("DB_HOST", default="postgres")
POSTGRES_PASSWORD = env("DB_PASS", default="")
POSTGRES_USER = env("DB_USER", default="zadanie")

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}",
    ),
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

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_HOSTNAME = env("REDIS_HOSTNAME", default="redis")
REDIS_HOSTNAME_FOR_WEBSOCKETS = env("REDIS_HOSTNAME_FOR_WEBSOCKETS", default="redis")
REDIS_PORT = 6379
REDIS_CELERY_BROKER_DB = env.int("REDIS_CELERY_BROKER_DB", 0)
REDIS_CELERY_RESULT_BACKEND_DB = env.int("REDIS_CELERY_RESULT_BACKEND_DB", 1)
REDIS_MAIN_DB = env.int("REDIS_MAIN_DB", 2)
REDIS_SESSION_DB = env.int("REDIS_SESSION_DB", 3)

KEY_PREFIX_SESSION = "zadanie-session"
CACHE_VERSION = 2
KEY_PREFIX = "zadanie"
KEY_FUNCTION = "apps.common.utils.make_cache_key"

REDIS_CACHE = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": f"redis://{REDIS_HOSTNAME}/{REDIS_MAIN_DB}",
    "OPTIONS": {"health_check_interval": 30},
    "KEY_PREFIX": KEY_PREFIX,
    "VERSION": CACHE_VERSION,
    "KEY_FUNCTION": KEY_FUNCTION,
}

REDIS_SESSION_CACHE = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": f"redis://{REDIS_HOSTNAME}/{REDIS_SESSION_DB}",
    "OPTIONS": {"health_check_interval": 30},
    "KEY_PREFIX": KEY_PREFIX_SESSION,
    "VERSION": CACHE_VERSION,
    "KEY_FUNCTION": KEY_FUNCTION,
}

CACHES = {"default": REDIS_CACHE, "session": REDIS_SESSION_CACHE}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'url_create': '50/day',
        'url_retrieve': '1000/day',
        'url_original': '2000/day',
    }
}
