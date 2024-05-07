#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic

# Build the project
python3 manage.py build
