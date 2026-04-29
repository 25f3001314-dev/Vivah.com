#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Vedic Matchmaking API
Run with: python main.py
"""

if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from v1 import app

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid double imports
        log_level="info",
        access_log=True,
    )
