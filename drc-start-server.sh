#!/usr/bin/env bash

(cd menumanager_country_api; gunicorn --env DJANGO_SETTINGS_MODULE=$SETTINGS_PATH menumanager_country_api.wsgi --user www-data --bind 0.0.0.0:20243 --workers 2 --timeout 120  --worker-class=gevent --worker-connections=1000)