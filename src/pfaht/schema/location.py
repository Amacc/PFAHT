from pydantic import BaseModel


class Location(BaseModel):
    """
    Location Schema
    ================
    """

    location_name: str
    location_description: str
    location_address: str
    location_city: str
    location_state: str
    location_zip: int
    location_country: str

    @property
    def _html_template(self):
        return "location/item.html"

    def __str__(self):
        return self.location_name

    def __repr__(self):
        return f"Location({self.location_name})"
