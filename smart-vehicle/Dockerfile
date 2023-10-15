# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY key.pem key.pem
COPY cert.pem cert.pem

CMD ["python", "main.py"]