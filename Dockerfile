FROM python:3-stretch

WORKDIR /menumanager_country_api
RUN pwd
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/menumanager_country_api

COPY requirements.txt kenya-start-server.sh /opt/app/

COPY . /opt/app/menumanager_country_api/

RUN groupadd -r docker -g 1000 \
	&& useradd -u 1000 -r -g docker -d /opt/app -s /sbin/nologin -c "Docker image user" docker \
	&& chown -R docker:docker /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt --no-cache-dir
ENV PATH="/opt/app/.local/bin:${PATH}"

USER docker
RUN chmod 775 /opt/app/kenya-start-server.sh

STOPSIGNAL SIGTERM
