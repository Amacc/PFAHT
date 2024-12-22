from pydantic import BaseModel


class Link(BaseModel):
    url: str
    title: str
    method: str = "GET"
    _htmx: bool = True


class AnchorLink(Link):
    _htmx: bool = False


class Index(BaseModel):
    _html_template: str = "index.html"
    links: dict[str, Link | AnchorLink] = {
        "Devices": Link(url="/devices", title="Devices"),
        "Issues": Link(url="/issues/", title="Issues"),
        "Users": Link(url="/users", title="Users"),
        "Docs": AnchorLink(url="/docs", title="API Documentation"),
        "ReDoc": AnchorLink(url="/redoc", title="API Documentation (ReDoc)"),
        "OpenApiJSON": AnchorLink(url="/openapi.json", title="OpenAPI JSON"),
    }
