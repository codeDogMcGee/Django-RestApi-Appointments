# syntax=docker/dockerfile:1
FROM python:3.9.5-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# install psycopg2 dependencies
RUN apt-get update && apt-get install
RUN apt-get install -y gcc && apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/