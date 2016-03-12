FROM python:3.4

MAINTAINER Miguel Ángel Durán <hi@mangel.me>

ENV APP_HOME /opt/app/

ADD . /opt/app/

WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/* && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python", "manage.py"]
