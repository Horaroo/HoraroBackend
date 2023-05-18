FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG DEV=false

RUN pip install --upgrade pip && pip install "poetry==1.4.1"

RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN pip install psycopg2-binary --no-binary psycopg2-binary

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    if [ $DEV = "true" ];  \
      then poetry install --no-interaction --no-ansi ; \
    else poetry install --no-interaction --no-ansi --without dev ; \
    fi



COPY . .


RUN find . -type f -exec chmod 644 {} \; && \
    adduser --disabled-password --no-create-home john-doe && chmod 755 manage.py && \
    find . -type d -exec chmod 755 {} \;

RUN python /app/manage.py collectstatic --noinput

RUN touch app.log && chown john-doe:john-doe app.log

USER john-doe