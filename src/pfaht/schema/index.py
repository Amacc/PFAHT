from pydantic import BaseModel


class Link(BaseModel):
    url: str
    title: str
    method: str = "GET"


class Index(BaseModel):
    _html_template: str = "index.html"
    links: dict[str, Link] = {
        "Devices": Link(url="/devices", title="Devices"),
        "Issues": Link(url="/issues/", title="Issues"),
        "Users": Link(url="/users", title="Users"),
        "Docs": Link(url="/docs", title="API Documentation"),
        "ReDoc": Link(url="/redoc", title="API Documentation (ReDoc)"),
        "OpenApiJSON": Link(url="/openapi.json", title="OpenAPI JSON"),
    }
