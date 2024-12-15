"""
Schema for devices
==================
"""

from pydantic import BaseModel, ConfigDict

from . import api, index


class NewDevice(BaseModel):

    device_name: str
    device_type: str
    device_location: str

class Device(NewDevice):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    device_id: int

class MissingDeviceResponse(api.ApiResponse[None]):
    ...

class DeviceListResponse(api.ApiResponse[list[Device]]):
    @property
    def _html_template(self):
        return "device/list.html"

class DeviceResponse(api.ApiResponse[Device]):
    @property
    def _html_template(self):
        return "device/item.html"

    def model_post_init(self, __context):
        self.links = [
            index.Link(
                url=f"/devices/{self.response.device_id}",
                title=f"{self.response.device_id} - {self.response.device_name}"
            ),
            index.Link(
                url=f"/devices/{self.response.device_id}/edit",
                title="Edit",
                style="btn btn-primary"
            )
        ]

class DeviceCreatedResponse(DeviceResponse):
    message: str = "Device created successfully"
