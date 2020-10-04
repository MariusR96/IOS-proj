FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH


WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
