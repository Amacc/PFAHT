from pydantic import BaseModel


class Link(BaseModel):
    url: str
    title: str

class Index(BaseModel):
    _html_template: str = "index.html"
    links: list[Link] = [
        Link(url="/devices", title="Devices"),
        Link(url="/issues/", title="Issues"),
        Link(url="/users", title="Users"),
        Link(url="/docs", title="API Documentation"),
        Link(url="/redoc", title="API Documentation (ReDoc)"),
        Link(url="/openapi.json", title="OpenAPI JSON"),
    ]
