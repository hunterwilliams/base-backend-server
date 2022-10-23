#!/usr/bin/env bash

echo "Cards Server start!"
cd ./cards-server-app
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# python manage.py init_super_user
python manage.py runserver 0.0.0.0:8000
