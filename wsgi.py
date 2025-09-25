"""
WSGI entry point for Railway deployment
This file helps Railway detect this as a Flask application
"""

from app import app

if __name__ == "__main__":
    app.run()