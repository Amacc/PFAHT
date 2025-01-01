"""
PFAHT Web Routes
================

This module contains the FastAPI routers for the web app server.
"""

from fastapi import FastAPI, Depends

from . import auth, devices, device_types, issues, users


def install_routes(app: FastAPI):
    for router in [
        auth.router,
        devices.router,
        device_types.router,
        issues.router,
        users.router,
    ]:
        app.include_router(router, dependencies=[Depends(auth.current_user())])
