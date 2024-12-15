from logging import getLogger
from fastapi import APIRouter, Depends, Request

from ... import schema, services
from .. import html

logger = getLogger(__name__)
router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("")
@html.content_negotiation()
async def list_devices(
    _request: Request,
    device_list = Depends(services.devices.list_devices)
):
    """List all devices"""
    return schema.devices.DeviceListResponse(response=device_list)

@router.get("/{device_id}")
async def get_device(
    device = Depends(services.devices.get_device)
):
    """Get a device by ID"""
    return schema.devices.DeviceResponse(response=device)

@router.get("/init")
async def install_devices_table(
    install_result = Depends(services.devices.create_device_table)
):
    """Initialize the devices table"""
    logger.debug(f"{install_result=}")
    return {"message": "Device table created"}

@router.post("")
def create_device(
    created_device: schema.devices.NewDevice = Depends(services.devices.create_device)
):
    """
    Create a new device
    """
    return schema.devices.DeviceCreatedResponse(response=created_device)