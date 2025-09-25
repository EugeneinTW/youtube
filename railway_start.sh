#!/bin/bash

# Railway startup script for Flask app
# Handle PORT environment variable properly

# Set default port if PORT is not set or invalid
if [ -z "$PORT" ] || ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    PORT=8080
    echo "Using default port: $PORT"
else
    echo "Using Railway port: $PORT"
fi

# Start gunicorn with the correct port
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120