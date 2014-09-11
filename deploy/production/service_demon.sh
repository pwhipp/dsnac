#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/dsnac/.virtualenvs/production/bin/activate
source /home/dsnac/.virtualenvs/production/bin/postactivate

cd /home/dsnac/production

exec gunicorn -c /home/dsnac/production/deploy/gunicorn.conf.py core.wsgi:application