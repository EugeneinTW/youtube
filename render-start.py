#!/usr/bin/env python3
"""
Render-specific startup script for Streamlit
Ensures proper configuration for Render deployment
"""

import os
import subprocess
import sys

def main():
    # Get port from environment
    port = os.environ.get('PORT', '10000')
    
    print(f"Starting Streamlit on Render with port {port}")
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    
    # Streamlit command for Render
    cmd = [
        'streamlit', 'run', 'app.py',
        f'--server.port={port}',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--server.enableCORS=false',
        '--server.enableXsrfProtection=false'
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    
    # Execute streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Streamlit not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'streamlit'], check=True)
        subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()