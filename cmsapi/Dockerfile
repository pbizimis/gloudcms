#Dockerfile for the GloudCMS admin interface
FROM python:3.7.3-stretch

LABEL maintainer="philip.bizimis@code.berlin"
LABEL version="1.0"

#set workdir and copy files
WORKDIR /cmsapi
COPY apiapp apiapp/
COPY wsgi.py .
COPY requirements.txt .

#set and activate virtual environment
ENV VIRTUAL_ENV="/venv"
RUN python3.7 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#install dependencies
RUN pip install -r requirements.txt

EXPOSE 8081

CMD ["gunicorn", "-b", "0.0.0.0:8081", "--workers=3","wsgi:app"]