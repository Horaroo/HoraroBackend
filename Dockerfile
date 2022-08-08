FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app



COPY requirements.txt requirements.txt


RUN pip3 install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 188.225.39.190:8000