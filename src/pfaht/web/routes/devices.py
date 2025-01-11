from logging import getLogger
from fastapi import APIRouter, Depends, Request

from ... import schema, services
from .. import html

logger = getLogger(__name__)
router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/init")
async def install_devices_table(
    install_result=Depends(services.devices.create_device_table),
):
    """Initialize the devices table"""
    logger.debug(f"{install_result=}")
    return {"message": "Device table created"}


@router.get("", response_model=schema.devices.DeviceListResponse)
@html.content_negotiation()
async def list_devices(
    _request: Request, device_list=Depends(services.devices.list_devices)
):
    """List all devices"""
    return schema.devices.DeviceListResponse(response=device_list)


@router.get("/{device_id}", response_model=schema.devices.DeviceResponse)
@html.content_negotiation()
async def get_device(_request: Request, device=Depends(services.devices.get_device)):
    """Get a device by ID"""
    return schema.devices.DeviceResponse(response=device)


@router.put("/{device_id}", response_model=schema.devices.DeviceResponse)
@html.content_negotiation()
async def update_device(
    _request: Request, device=Depends(services.devices.update_device)
):
    """Update a device by ID"""
    return schema.devices.DeviceResponse(response=device)


@router.delete("/{device_id}", response_model=schema.devices.DeletedDeviceResponse)
@html.content_negotiation()
async def delete_device(
    _request: Request,
    device_id: int,
    delete_response=Depends(services.devices.delete_device),
):
    """Update a device by ID"""
    return schema.devices.DeletedDeviceResponse(response=device_id)


@router.post("", response_model=schema.devices.DeviceCreatedResponse)
def create_device(
    created_device: schema.devices.NewDevice = Depends(services.devices.create_device),
):
    """
    Create a new device
    """
    return schema.devices.DeviceCreatedResponse(response=created_device)


@router.get("/{device_id}/issues", response_model=schema.issues.IssueListResponse)
def list_assigned_issues(
    issue_list: schema.issues.IssueListServiceResponse = Depends(
        services.issues.list_issues_for_device
    ),
):
    """List all issues assigned to a device"""
    return schema.issues.IssueListResponse(response=issue_list.data)
