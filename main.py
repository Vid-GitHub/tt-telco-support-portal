#!/usr/bin/env python3
"""
Main entry point for TT Telco Support Portal
"""

import os
from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting TT Telco Support Portal on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)