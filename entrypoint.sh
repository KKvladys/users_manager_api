#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT"; do
  sleep 2
done
echo "PostgreSQL is ready!"

echo "Applying database migrations..."
flask --app run db upgrade

echo "Starting the Flask app..."
exec flask --app run run --host=0.0.0.0

