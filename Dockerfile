FROM python:3.11-slim

WORKDIR /bot

COPY requirements.txt .

RUN apt-get -y update && RUN apt-get -y upgrade && pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .