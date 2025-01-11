"""
Schema for devices
==================
"""

from pydantic import BaseModel, ConfigDict, Field

from . import api, index, services

DeviceId = int


class NewDevice(BaseModel):
    """
    New Device Schema
    =================

    """

    device_name: str
    device_type: str
    device_location: str


class Device(NewDevice):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    device_id: DeviceId


class MissingDeviceResponse(api.ApiResponse[None]):
    message: str = "Device not found"


class DeviceListResponse(api.ApiResponse[list[Device]]):
    _header_links: list[str] = {
        "NewForm": index.Link(url="/devices/new", title="New Device"),
    }

    @property
    def title(self):
        return "Device List"

    @property
    def _html_template(self):
        return "page/list.html"


class DeviceResponse(api.ApiResponse[Device]):
    @property
    def _html_template(self):
        return "page/detail.html"

    def model_post_init(self, __context):
        self.links = [
            index.Link(
                url=f"/devices/{self.response.device_id}",
                title=f"{self.response.device_id} - {self.response.device_name}",
            ),
            index.Link(
                url=f"/devices/{self.response.device_id}/edit",
                title="Edit",
                style="btn btn-primary",
            ),
        ]


class DeletedDeviceResponse(api.ApiResponse[DeviceId]):
    message: str = "Device deleted successfully"


class DeviceCreatedResponse(DeviceResponse):
    message: str = "Device created successfully"


class DeviceType(BaseModel):
    """
    Device Type Schema
    ==================

    """

    device_type: str
    links: dict[str, index.Link] = Field(default_factory=dict)

    def model_post_init(self, __context):
        self.links = {
            "self": index.Link(
                url=f"/device-types/{self.device_type}",
                title=f"{self.device_type}",
            )
        }


class DeviceTypeListResponse(api.ApiResponse[list[DeviceType]]):
    @property
    def title(self):
        return "Device Types"

    @property
    def _html_template(self):
        return "page/list.html"


class DeviceServiceResponse(services.ServiceResponse[Device]):
    """Device Service Response Schema"""


class DeviceListServiceResponse(services.ServiceResponseList[Device]):
    """Device List Service Response Schema"""
