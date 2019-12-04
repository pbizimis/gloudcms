#!/bin/bash
source venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=apiapp
export FLASK_RUN_PORT=5000
export MONGO_IP=127.0.0.1
flask run

