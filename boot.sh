#!/bin/bash
ADMIN_LOGIN=$ADMIN_LOGIN ADMIN_PASSWORD=$ADMIN_PASSWORD python init.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - main:app