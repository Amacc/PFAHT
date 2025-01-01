from logging import getLogger
from fastapi import APIRouter, Depends, Request, Form, Body
from typing import Annotated

from ... import schema, services
from .. import html

logger = getLogger(__name__)
router = APIRouter(prefix="/issues", tags=["Issues"])


@router.get("/init", response_model=schema.issues.IssueTableCreatedResponse)
async def init_issues_tables(
    issues_table=Depends(services.issues.create_issue_table),
    related_devices_table=Depends(services.issues.create_related_devices_table),
) -> schema.issues.IssueTableCreatedResponse:
    """Initialize the Issues table"""
    logger.debug(f"{issues_table=}; {related_devices_table=}")

    return schema.issues.IssueTableCreatedResponse()


@router.get("/new")
@html.content_negotiation()
async def new_issue(_request: Request):
    """Get a valid new issue"""
    # return schema.issues.DefaultIssue()
    # return schema.api.ApiResponse(
    return schema.issues.DefaultIssueResponse(
        response=schema.issues.DefaultIssue(),
    )


@router.get("", response_model=schema.issues.IssueListResponse)
@html.content_negotiation()
async def list_issues(
    _request: Request,
    issue_list=Depends(services.issues.list_issues),
) -> schema.issues.IssueListResponse:
    """List all issues"""
    return schema.issues.IssueListResponse(
        response=issue_list.data, page_options=issue_list.page_options
    )


@router.get("/{issue_id}", response_model=schema.issues.IssueResponse)
@html.content_negotiation()
async def get_issue(
    _request: Request,
    issue: schema.issues.IssueServiceResponse = Depends(services.issues.get_issue),
) -> schema.issues.IssueResponse:
    """Get a issue by ID"""
    return schema.issues.IssueResponse(
        response=issue.data,
    )


@router.put("/{issue_id}", response_model=schema.issues.IssueResponse)
@html.content_negotiation()
async def update_issue(
    _request: Request,
    issue: schema.issues.IssueServiceResponse = Depends(services.issues.update_issue),
) -> schema.issues.IssueResponse:
    """Update a issue by ID"""
    return schema.issues.IssueResponse(response=issue.data)


@router.delete("/{issue_id}", response_model=schema.issues.DeletedIssueResponse)
@html.content_negotiation()
async def delete_issue(
    _request: Request,
    issue_id: int,
    delete_response=Depends(services.issues.delete_issue),
) -> schema.issues.DeletedIssueResponse:
    """Delete issue by ID"""
    return schema.issues.DeletedIssueResponse(response=issue_id)


@router.post("", response_model=schema.issues.IssueResponse)
def create_issue(
    created_issue: schema.issues.NewIssue = Depends(services.issues.create_issue),
):
    """
    Create a new issue
    """
    return schema.issues.IssueResponse(response=created_issue)


@router.get("/{issue_id}/devices", response_model=schema.issues.RelatedDevicesResponse)
@html.content_negotiation()
def get_related_devices(
    _request: Request,
    issue_id: int,
    related_devices=Depends(services.issues.get_related_devices),
):
    """Get all devices related to an issue"""
    return schema.issues.RelatedDevicesResponse(
        response=related_devices,
        issue_id=issue_id,
    )


@router.put(
    "/{issue_id}/devices/relate/{device_id}",
    response_model=schema.issues.RelateDeviceResponse,
)
@html.content_negotiation()
def relate_device(
    _request: Request,
    related_device: schema.issues.RelateDeviceResponse = Depends(
        services.issues.relate_device
    ),
):
    """Relate a device to an issue"""
    return schema.issues.RelateDeviceResponse(response=related_device.response)


@router.put(
    "/{issue_id}/devices/relate",
    response_model=schema.issues.RelateDeviceResponse,
)
@html.content_negotiation()
def relate_device(
    _request: Request,
    related_device: schema.issues.RelateDeviceResponse = Depends(
        services.issues.relate_device_from_schema
    ),
):
    """Relate a device to an issue"""
    return schema.issues.RelateDeviceResponse(response=related_device.response)
