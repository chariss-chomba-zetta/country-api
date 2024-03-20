FROM python:3-stretch

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -


RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql17 unixodbc-dev -y

# copy source and install dependencies
WORKDIR /menumanager_country_api
RUN pwd
RUN ls -la

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/menumanager_country_api

COPY ../ /opt/app/menumanager_country_api/
RUN ls -la /opt/app/menumanager_country_api/
RUN ls -la /opt/app
WORKDIR /opt/app


RUN pip install -r requirements.txt --no-cache-dir

RUN chown -R www-data:www-data /opt/app
RUN chmod +x /opt/app/kenya-start-server.sh

# start server
EXPOSE 20254
STOPSIGNAL SIGTERM
CMD ["/opt/app/kenya-start-server.sh"]
