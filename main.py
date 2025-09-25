#!/usr/bin/env python3
"""
Main entry point for Render deployment
This file ensures Render starts the application correctly
"""

import os
import sys
import subprocess

def main():
    """Main function to start the Streamlit application"""
    
    # Get port from environment (Render sets this)
    port = os.environ.get('PORT', '10000')
    
    print(f"🚀 Starting YouTube Downloader on port {port}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Set environment variables for Streamlit
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    
    # Command to run Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        f'--server.port={port}',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--server.enableCORS=false',
        '--server.enableXsrfProtection=false'
    ]
    
    print(f"🔧 Executing command: {' '.join(cmd)}")
    
    try:
        # Run the command
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())