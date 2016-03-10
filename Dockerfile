FROM python:3.5.1-alpine

MAINTAINER Miguel Ángel Durán <hi@mangel.me>

ENV APP_HOME /opt/app/

WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME

RUN pip3 install -r requirements.txt

