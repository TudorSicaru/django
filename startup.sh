#!/bin/bash

# Start the redis server
service redis-server start

# Start the django server
python3 manage.py runserver 0.0.0.0:8000
