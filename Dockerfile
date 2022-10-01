FROM python:3-alpine


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --upgrade pip && apk add build-base && \
        pip3 install -r requirements.txt && \
        echo 'root:awdkj%W@!#' | chpasswd

RUN  adduser --disabled-password --no-create-home john-doe

USER john-doe
