#Dockerfile for the GloudCMS admin interface
FROM python:3.7.3-stretch

LABEL maintainer="philip.bizimis@code.berlin"
LABEL version="1.0"

#set workdir and copy files
WORKDIR /gloudcmsd
COPY interfaceapp interfaceapp/
COPY wsgi.py .
COPY requirements.txt .

#set and activate virtual environment
ENV VIRTUAL_ENV="/venv"
RUN python3.7 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#install dependencies
RUN pip install -r requirements.txt

#change this when building
ENV JWT_SECRET 0000

EXPOSE 8080

CMD ["gunicorn", "-b", "127.0.0.1:8080", "--workers=3","wsgi:app"]