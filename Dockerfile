FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


# RUN apt-get update && apt-get install -qq -y \
#   build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /tournament
RUN mkdir -p $INSTALL_PATH


WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .
# RUN pip install --editable .
