FROM python:3.5.1-alpine

MAINTAINER Miguel Ángel Durán <hi@mangel.me>

ENV APP_HOME /opt/app/

ADD . /opt/app/

WORKDIR $APP_HOME

RUN apk --update add postgresql-client

RUN apk --update add --virtual build-dependencies \
    build-base \
    python3-dev \
    postgresql-dev \
    zlib zlib-dev curl jpeg jpeg-dev libpng libpng-dev && \
    pip3 install -r requirements.txt && \
    apk del build-dependencies && \
    rm -f /var/cache/apk/*

ENTRYPOINT ["python", "manage.py"]
