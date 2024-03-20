# from .base import *

# # todo - update to the real db, allowed hosts, etc
# ALLOWED_HOSTS = ['*']
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': os.environ['DATABASE_NAME'],
#         'USER': '#{USSD-SQLDB1-USERNAME}#',
#         'PASSWORD': '#{USSD-SQLDB1-PASWORD}#',
#         'HOST': '#{USSD-SQLDB1-HOSTNAME}#',
#         'PORT': '1433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server'
#         },
#     },
# }

from .base import *

# todo - update to the real db, allowed hosts, etc
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': '#{USSD-SQLDB1-USERNAME}#',
        'PASSWORD': '#{USSD-SQLDB1-PASWORD}#',
        'HOST': '#{USSD-SQLDB1-HOSTNAME}#',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server'
        },
    },
}
