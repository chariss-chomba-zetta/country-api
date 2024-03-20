#!/usr/bin/env bash

cd menumanager_country_api || exit
(gunicorn menumanager_country_api.wsgi --bind 0.0.0.0:"$(( $SERVICE_BASE_PORT + $COUNTRY_CODE ))" --workers 1 --timeout 120)
