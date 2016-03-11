FROM node:5.8

ENV APP_HOME /opt/app

WORKDIR $APP_HOME

RUN npm install -g bower -g gulp

RUN useradd -m -U node

USER node
