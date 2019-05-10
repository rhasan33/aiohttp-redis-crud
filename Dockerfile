FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app
RUN mkdir src

ADD requirements.txt /app
ADD wait-for-it.sh /app

RUN apt-get update && apt-get install build-essential curl -y && \
    pip3 install -r requirements.txt && \
    apt-get --purge autoremove build-essential -y

COPY src/ /app/src/

EXPOSE ${PORT}
