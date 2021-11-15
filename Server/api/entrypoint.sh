#!/bin/sh
export SKIP_ZEROMQ=True
python3 care_api/manage.py makemigrations --noinput
python3 care_api/manage.py migrate
DJANGO_SUPERUSER_PASSWORD=test python3 care_api/manage.py createsuperuser --username test --email test@gamil.com --noinput
unset SKIP_ZEROMQ
python3 care_api/manage.py runserver 0.0.0.0:8000 
# python3 care_api/manage.py runsslserver 0.0.0.0:8000 --certificate cert_key/cert.pem --key cert_key/key.pem