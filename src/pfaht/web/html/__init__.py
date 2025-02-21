from asyncio import iscoroutine
from functools import wraps
from pathlib import Path
from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ... import schema

logger = getLogger(__name__)
template_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=template_path)

static_path = Path(__file__).parent / "static"
print(f"Static Path: {static_path}")
static = StaticFiles(directory=static_path)

_cached_templates = {}


def camel_to_kebab(string: str) -> str:
    """Convert a camel case string to kebab case"""
    return "".join(["-" + c.lower() if c.isupper() else c for c in string]).lstrip("-")


def template_exists(template_name: str) -> bool:
    """Check if a template exists"""
    if template_name in _cached_templates:
        return _cached_templates[template_name]
    try:
        exists = templates.get_template(template_name) is not None
    except Exception:
        exists = False
    _cached_templates[template_name] = exists
    return exists


def template_path_from_request(request: Request):
    """Get the template path from the request"""
    # template_base_path = request.url.path.lstrip("/")
    template_base_path = request.url.path.split("/")[1]
    template_format = request.query_params.get("format", "detail")
    return f"{template_base_path}/{template_format}.html"


def template_path_from_item(item: any, request: Request):
    """Get the template path based on a request and an item"""
    if template_path := getattr(item, "_template_path", None):
        template_base_path = template_path
    elif plural := getattr(item, "plural", None):
        template_base_path = plural
    else:
        template_base_path = camel_to_kebab(item.__class__.__name__)
    template_format = request.query_params.get("format", "detail")
    return f"{template_base_path}/{template_format}.html"


def configure_templates(app: FastAPI):
    #  configure the template environment filters
    templates.env.globals["app_name"] = app.title
    templates.env.globals["app"] = app.version
    templates.env.globals["menu"] = schema.index.Index().links
    templates.env.filters["is_htmx_request"] = (
        lambda x: x.headers.get("HX-Request", None) == "true"
    )
    templates.env.filters["template_exists"] = template_exists
    templates.env.filters["template_path_from_request"] = template_path_from_request
    templates.env.filters["template_path_from_item"] = template_path_from_item


def content_negotiation():
    """Decorator that will check the Accept header and return the appropriate response]

    Requires that you have the request object as a parameter in the decorated function
    """

    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            function_response = f(*args, **kwargs)
            if iscoroutine(function_response):
                response = await function_response
            else:
                response = function_response

            # Requires that the request object is passed in as a parameter
            if not (request := kwargs.get("_request", kwargs.get("request", None))):
                logger.info("Skipping HTML Parsing; Request object not found in kwargs")
                return response

            # Check if the request has an Accept header
            logger.info(f"Request Headers: {request.headers}")
            if not (accept_header := request.headers.get("Accept", None)):
                logger.info("No Accept header found")
                return response

            html_found = False
            for html_accept in ["text/html", "application/xhtml+xml"]:
                if html_accept in accept_header:
                    html_found = True
                    break

            if not html_found:
                logger.info("No HTML Accept header found")
                return response

            # Transform the response into an html response if the return
            # has an _html or _html_template attribute.
            if hasattr(response, "_html"):
                logger.info(f"Returning HTML: {response._html}")
                return HTMLResponse(content=response._html)

            if hasattr(response, "_html_template"):
                logger.info(f"Rendering template: {response._html_template}")
                return templates.TemplateResponse(
                    request=request,
                    name=response._html_template,
                    context={"item": response},
                )

            return response

        return wrapper

    return decorator
