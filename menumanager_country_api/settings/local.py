from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/vas.sqlite3'),
        # 'NAME': BASE_DIR / str(os.environ["LOCAL_DATABASE_NAME"]),
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": 'country_api_db',
    #     "USER": 'postgres',
    #     "PASSWORD": 'postgres',
    #     "HOST": 'db',
    #     "PORT": 5432,
    #     # 'OPTIONS': {
    #     #     'options': '-c search_path=menu_migration',
    #     # }
    # }
}



REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_SSL = os.environ.get('REDIS_SSL') == 'True'
REDIS_SSL_CERT = os.environ.get('REDIS-SSL-CERT')
REDIS_RUNS_IN_CLUSTER = os.environ.get('REDIS_RUNS_IN_CLUSTER') == 'True'
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
