#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

#until python manage.py check --database default > /dev/null 2>&1
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
do
    sleep 2
done

echo "Database is ready."

# Move into the Django project
cd /app/careerforge_backend

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn careerforge_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 180