import logging

from .base import *

LOGGING['handlers'].update(
    {
        'gunicorn': {
            'class': 'logging.StreamHandler',
        },
    },
)
LOGGING['loggers'].update(
    {
        'gunicorn': {
            'handlers': ['gunicorn'],
            'level': 'INFO',
            'propagate': False,
        },
    },
)

logger = logging.getLogger('gunicorn')

print('*' * 50)
print(f'Running with local files in: {str(__file__)}')
logger.info('Running with local files in: %s', {str(__file__)})
print(f'COUNTRY CODE: {str(COUNTRY_CODE)}')
logger.info('COUNTRY: %s', str(COUNTRY_CODE))
print(f'DB: {str(BASE_DIR)} / {str(os.environ["LOCAL_DATABASE_NAME"])}')
logger.info('DB: %s / %s', str(BASE_DIR), str(os.environ["LOCAL_DATABASE_NAME"]))
print('*' * 50)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / str(os.environ["LOCAL_DATABASE_NAME"]),
    }
}
# USE_TZ = True
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': os.environ['DATABASE_NAME'],
#         'USER': 'sql-equity-admin',
#         'PASSWORD': 'h3xzqqc73Tigy84pEiHQQPQap',
#         'HOST': 'equity-dev-test-001.database.windows.net',
#         'PORT': '1433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server'
#         },
#     },
# }

REDIS_SSL = False
REDIS_RUNS_IN_CLUSTER = False
