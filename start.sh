#!/bin/bash

# Railway startup script
# Use fixed port to avoid environment variable issues
FIXED_PORT=8080

echo "Starting Streamlit on port $FIXED_PORT"

# Check if PORT environment variable exists and is numeric
if [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Using Railway PORT: $PORT"
    FIXED_PORT=$PORT
else
    echo "PORT not set or invalid, using default: $FIXED_PORT"
fi

streamlit run app.py \
  --server.port $FIXED_PORT \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false