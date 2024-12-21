"""
PFAHT Web Routes
================

This module contains the FastAPI routers for the web app server.
"""

from fastapi import FastAPI

from . import devices, device_types, issues


def install_routes(app: FastAPI):
    for router in [devices.router, device_types.router, issues.router]:
        app.include_router(router)
