from asyncio import iscoroutine
from functools import wraps
from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .. import __version__, dist_name, schema
from . import html
from .routes import install_routes

logger = getLogger(__name__)
app = FastAPI(
    title=dist_name,
    version=__version__,
)
app.mount("/static", html.static, name="static")
install_routes(app)
html.configure_templates(app)

@app.get("/")
@html.content_negotiation()
def read_root(_request: Request):
    return schema.index.Index()

if __name__ == "__main__":
    # Launch the FastAPI app using Uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

