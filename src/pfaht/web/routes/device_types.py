from fastapi import APIRouter, Depends, Request

from ... import services, schema
from .. import html

router = APIRouter(prefix="/device-types", tags=["Device Types"])


@router.get("")
@html.content_negotiation()
async def list_device_types(
    _request: Request,
    device_types=Depends(services.devices.list_device_types),
):
    """List all device types"""
    return schema.devices.DeviceTypeListResponse(response=device_types)
