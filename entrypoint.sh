#!/bin/bash

set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking if superuser exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='salman_ahamed').exists():
    User.objects.create_superuser(username='salman_ahamed', email='', password='s@lman5900')
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p 8000 mark1.asgi:application
