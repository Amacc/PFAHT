"""
Web Application Entry Point
===========================
"""

from logging import getLogger

from fastapi import FastAPI, Request


from .. import __version__, dist_name, schema, config
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


@app.get("/", tags=["Index"])
@html.content_negotiation()
def app_index(_request: Request):
    """APP Index"""
    return schema.index.Index()


if __name__ == "__main__":
    # Launch the FastAPI app using Uvicorn
    import uvicorn
    uvicorn.run(
        "pfaht.web.app:app" if config.FAST_API_RELOAD else app,
        host=config.FAST_API_HOST,
        port=config.FAST_API_PORT,
        reload=config.FAST_API_RELOAD,
    )
