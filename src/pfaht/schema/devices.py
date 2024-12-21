"""
Schema for devices
==================
"""

from pydantic import BaseModel, ConfigDict

from . import api, index

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
    @property
    def _html_template(self):
        return "device/item.html"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    device_id: DeviceId


class MissingDeviceResponse(api.ApiResponse[None]):
    message: str = "Device not found"


class DeviceListResponse(api.ApiResponse[list[Device]]):
    @property
    def _title(self):
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


class DeviceTypeListResponse(api.ApiResponse[list[str]]):
    @property
    def _html_template(self):
        return "page/list.html"
