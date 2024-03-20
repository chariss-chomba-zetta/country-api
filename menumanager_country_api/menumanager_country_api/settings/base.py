import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'base_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menus',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'menumanager_country_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'menumanager_country_api.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# MSSQL DOES NOT FULLY SUPPORT TIMEZONES.
USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname}-{asctime} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'CountryApiLogger': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        },
    }
}

# --------------------------REDIS SETTINGS--------------------------
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_SSL = os.environ.get('REDIS_SSL') == 'True'
REDIS_SSL_CERT = os.environ.get('REDIS-SSL-CERT')
REDIS_RUNS_IN_CLUSTER = os.environ.get('REDIS_RUNS_IN_CLUSTER') == 'True'

# For WHEN and ONLY WHEN Redis runs in a cluster, there should be another
# non-clustered instance to store temp DBs. That should be defined with the
# ENVs listed bellow.
if REDIS_RUNS_IN_CLUSTER:
    REDIS_TEMP_HOST = os.environ.get('REDIS_NON_CLUSTERED_HOST')
    REDIS_TEMP_PORT = os.environ.get('REDIS_NON_CLUSTERED_PORT')
    REDIS_TEMP_PASS = os.environ.get('REDIS_NON_CLUSTERED_PASS')
    REDIS_TEMP_SSL = os.environ.get('REDIS_NON_CLUSTERED_SSL') == 'True'

# --------------------------APP SETTINGS--------------------------
# When new countries are added, do not forget to add those here
SUPPORTED_COUNTRIES = {
    211: 'SS',
    250: 'RW',
    254: 'KE',
    255: 'TZ',
    256: 'UG',
}

SERVICE_BASE_PORT = int(os.environ.get('SERVICE_BASE_PORT', 20_000))
CACHE_MENU_KEY_PREFIX = os.environ.get('CACHE_MENU_KEY_PREFIX', 'menus')
COUNTRY_CODE = int(os.environ.get('COUNTRY_CODE'))
CACHE_OMNI_KEY_PREFIX = os.environ.get('CACHE_OMNI_KEY_PREFIX', 'OMNI')


CORS_ALLOWED_ORIGINS = [
    "https://ussd-menu-management-dev.azurewebsites.net"
]
