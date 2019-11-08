FROM python:3.7.3-stretch

WORKDIR /gloudcmsd

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY cmsapp cmsapp
COPY flask_start.sh ./

ENV FLASK_APP cmsapp

EXPOSE 8080

ENTRYPOINT ["./flask_start.sh"]