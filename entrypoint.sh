#!/bin/bash

# Exit on error
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the server
echo "Starting Daphne server..."
daphne -b 0.0.0.0 -p 8000 mark1.asgi:application
