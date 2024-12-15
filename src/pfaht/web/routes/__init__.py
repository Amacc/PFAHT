from fastapi import FastAPI

from . import devices


def install_routes(app: FastAPI):
    for router in [devices.router]:
        app.include_router(router)
        