#!/bin/sh -ex

python manage.py collectstatic --no-input --clear

exec "$@"
