FROM ubuntu

LABEL maintainer="philip.bizimis@code.berlin"
LABEL version="1.0"

RUN apt-get update

RUN apt-get install -y nginx

RUN rm -v /etc/nginx/nginx.conf

ADD nginx.conf /etc/nginx/