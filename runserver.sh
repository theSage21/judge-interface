#! /bin/bash
source env/bin/activate
cd webserver
python manage.py collectstatic --noinput
gunicorn website.wsgi:application --bind=127.0.0.1:8000 --log-file=-
# gunicorn website.wsgi:application --bind=unix:/home/ghost/dev/InterfaceJudge/gunicorn_socket --log-file=-
