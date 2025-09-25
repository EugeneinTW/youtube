#!/usr/bin/env python3
"""
Railway-specific startup script for Streamlit
Handles port configuration without environment variable issues
"""

import os
import subprocess
import sys

def main():
    # Get port from environment or use default
    port = os.environ.get('PORT', '8080')
    
    # Validate port is numeric
    try:
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            port = '8080'
    except (ValueError, TypeError):
        port = '8080'
    
    print(f"Starting Streamlit on port {port}")
    
    # Streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        f'--server.port={port}',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--server.enableCORS=false',
        '--server.enableXsrfProtection=false'
    ]
    
    # Execute streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()