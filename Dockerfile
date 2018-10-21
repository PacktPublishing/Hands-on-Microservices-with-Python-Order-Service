FROM python:3-alpine

MAINTAINER Peter Fisher

COPY ./app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk add --update \
    py-mysqldb \
    gcc \
    libc-dev \
    mariadb-dev \
  && pip install --upgrade pip  \
  && pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*

COPY ./app /app

CMD ["python", "app.py"]

