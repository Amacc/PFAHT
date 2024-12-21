from pydantic import BaseModel


class Link(BaseModel):
    url: str
    title: str
    method: str = "GET"
    _htmx: bool = True


class Index(BaseModel):
    _html_template: str = "index.html"
    links: dict[str, Link] = {
        "Devices": Link(url="/devices", title="Devices"),
        "Issues": Link(url="/issues/", title="Issues"),
        "Users": Link(url="/users", title="Users"),
        "Docs": Link(url="/docs", title="API Documentation", _htmx=False),
        "ReDoc": Link(url="/redoc", title="API Documentation (ReDoc)", _htmx=False),
        "OpenApiJSON": Link(url="/openapi.json", title="OpenAPI JSON", _htmx=False),
    }
