"""
Configuration Module
====================

This module contains the configuration for the FastAPI application.

"""

from os import getenv


FAST_API_RELOAD = getenv("FAST_API_RELOAD", "1") == "1"
"""Enable FastAPI auto-reload"""
FAST_API_PORT = int(getenv("FAST_API_PORT", "8000"))
"""FastAPI port to listen on"""
FAST_API_HOST = getenv("FAST_API_HOST", "0.0.0.0")
"""FastAPI host to listen on"""

GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
"""Google OAuth Client ID"""
GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")
"""Google OAuth Client Secret"""
GOOGLE_REDIRECT_URI = getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google")
"""Google OAuth Redirect URI"""
