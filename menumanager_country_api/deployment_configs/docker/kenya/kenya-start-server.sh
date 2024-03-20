#!/usr/bin/env bash

(cd menumanager_coutry_api; gunicorn --env DJANGO_SETTINGS_MODULE=$SETTINGS_PATH menumanager_coutry_api.wsgi --user www-data --bind 0.0.0.0:8010 --workers 9 --timeout 20  --worker-class=gevent --worker-connections=1000)