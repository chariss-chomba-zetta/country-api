FROM python:3-stretch



RUN echo "deb http://deb.debian.org/debian buster main" > /etc/apt/sources.list


RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    apt-get install unixodbc-dev -y

WORKDIR /menumanager_country_api
ENV SETTINGS_PATH=menumanager_country_api.settings.local
ENV SECRET_KEY=rj+cio6-qv9xjsppbx3u-01wk2q$mr0q26mdyy4s1@sz5-y0ul

#APP SETTINGS
ENV SERVICE_BASE_PORT=20000
ENV CACHE_MENU_KEY_PREFIX=menus
ENV COUNTRY_CODE=254
ENV DATABASE_NAME=ussd-menumanagement-uat-ke
ENV CACHE_OMNI_KEY_PREFIX=VAS
ENV LOCAL_DATABASE_NAME=vas.sqlite3

# REDIS SETTINGS
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_PASS=redis
ENV REDIS_SSL=False
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/menumanager_country_api

COPY requirements.txt kenya-start-server.sh /opt/app/

COPY . /opt/app/menumanager_country_api/

WORKDIR /opt/app

RUN pip install -r requirements.txt --no-cache-dir

RUN chown -R www-data:www-data /opt/app
RUN chmod +x /opt/app/kenya-start-server.sh

# start server
EXPOSE 20254
# STOPSIGNAL SIGTERM
CMD ["/opt/app/kenya-start-server.sh"]
