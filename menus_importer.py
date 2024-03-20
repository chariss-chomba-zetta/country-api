"""
This is a support script that adds current production database dump
to your local docker-compose codebase.
What it does:
    Back-up any existing current local DBs
    Reads the menu data for countries listed in SUPPORTED_COUNTRIES
    Tries to load this menu using `loaddata` Django command
    Converts and changes some DB values for local usage
    Crates super-user with SUPERUSER_CREDENTIALS

By default, data should be placed here: `data_assets/menus_db_dumps`
"""

import datetime
import os
import sys
import traceback
from multiprocessing import Process
from pathlib import Path
from urllib.parse import urlparse

from menumanager_country_api.settings.base import SUPPORTED_COUNTRIES

SUPPORTED_COUNTRY_CODES = [d_val for d_key, d_val in SUPPORTED_COUNTRIES.items()]

# folder settings
BASE_DIR = Path(__file__).resolve().parent
ASSETS_FOLDER = os.path.join(BASE_DIR, 'data_assets')
DUMPS_FOLDER = os.path.join(ASSETS_FOLDER, 'menus_db_dumps')

# OTHERS
DJANGO_SETTINGS_MODULE = 'menumanager_country_api.settings.local'
DOCKER_COMPOSE_URL = 'ussd:8092'
SUPERUSER_CREDENTIALS = {
    'username': 'admin',
    'password': '1234',
}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _get_dumps_file_names():
    all_files = []
    for root, dirs, files in os.walk(DUMPS_FOLDER, followlinks=False):
        for file in files:
            if os.path.splitext(file)[-1] != '.json':
                continue
            all_files.append(file)
    return all_files


def _backup_old_dbs():
    for country_code in SUPPORTED_COUNTRY_CODES:
        filename = os.path.join(BASE_DIR, f'db_{country_code.lower()}.sqlite3')
        _backup_filename = f'db_{country_code.lower()}.' \
                           f'backup_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.sqlite3'
        backup_filename = os.path.join(BASE_DIR, _backup_filename)
        if os.path.exists(filename):
            print(f'Backing up old DB | {filename} -> {backup_filename}')
            os.rename(filename, backup_filename)


def _import_country(country_code, filename):
    # keep django imports here, so that those could be removed after completion of import
    import django
    from django.core.management import call_command
    from django.db import DatabaseError
    from django.db.models import Value
    from django.db.models.functions import Replace

    db_file = f'db_{country_code.lower()}.sqlite3'
    os.environ['LOCAL_DATABASE_NAME'] = db_file
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

    django.setup()
    from menus.models import OmniService
    from django.contrib.auth import get_user_model

    filename = f'data_assets/menus_db_dumps/{filename}'
    call_command('migrate')
    try:
        call_command('loaddata', filename, '-v 2')
    except DatabaseError:
        print(
            f'{bcolors.FAIL}[ERROR] There was an error when tried to import dump | '
            f'Country: {country_code}{bcolors.ENDC}')
        print(f'{bcolors.WARNING} Traceback | {str(traceback.format_exc())} {bcolors.ENDC}')
        print(f'Removing DB file {filename}...')
        os.remove(os.path.join(BASE_DIR, db_file))
        return

    # replace url with local docker-compose one
    url_parse = urlparse(OmniService.objects.first().url)
    print(f'Will replace: {url_parse.netloc} with {DOCKER_COMPOSE_URL} to work locally.')
    OmniService.objects.update(url=Replace('url', Value(url_parse.netloc), Value(DOCKER_COMPOSE_URL)))
    # create super-user
    get_user_model().objects.create_superuser(
        username=SUPERUSER_CREDENTIALS['username'],
        password=SUPERUSER_CREDENTIALS['password'],
    )
    print(f'{bcolors.OKGREEN}[SUCCESS] Country: {country_code} added successfully {bcolors.ENDC}')


def import_menus(country: str = None):
    _backup_old_dbs()

    all_files = _get_dumps_file_names()
    country_files = {country_code: filename for country_code in SUPPORTED_COUNTRY_CODES for filename in all_files
                     if filename.startswith(country_code)}
    if country is not None:
        country_files = {d_key: d_val for d_key, d_val in country_files.items() if d_key.lower() == country.lower()}

    for country_code, filename in country_files.items():
        p = Process(target=_import_country, kwargs={'country_code': country_code, 'filename': filename})
        p.start()
        p.join()


if __name__ == '__main__':
    country_arg = sys.argv[-1].upper()
    if country_arg in SUPPORTED_COUNTRY_CODES:
        import_menus(country=country_arg)
    else:
        import_menus()
