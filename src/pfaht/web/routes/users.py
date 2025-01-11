from fastapi import Response, APIRouter, Depends, Request
from ... import schema, services
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/init")
async def install_users_table(
    install_result=Depends(services.users.create_user_table),
):
    """Initialize the users table"""
    logger.debug(f"{install_result=}")
    return {"message": "User table created"}


@router.get("", response_model=schema.users.ListUserResponse)
def list_users(
    _request: Request,
    user_list=Depends(services.users.list_users),
):
    """List all users"""
    return schema.users.ListUserResponse(response=user_list)


@router.delete("/{user_id}", response_model=schema.users.DeleteUserResponse)
async def delete_user(
    user_id: str,
    delete_result=Depends(services.users.delete_user),
) -> schema.users.DeleteUserResponse:
    """Delete a user by ID"""
    return schema.users.DeleteUserResponse(response=bool(delete_result))


group_router = APIRouter(prefix="/groups", tags=["Groups"])


@group_router.get("", response_model=schema.users.ListGroupResponse)
async def list_groups(
    group_list: schema.users.GroupListServiceResponse = Depends(
        services.users.list_groups
    ),
) -> schema.users.ListGroupResponse:
    """List all groups"""
    return schema.users.ListGroupResponse(response=group_list.data)


@group_router.post("", response_model=schema.users.Group)
async def create_group(
    group: schema.users.GroupServiceResponse = Depends(services.users.create_group),
) -> schema.users.CreateGroupResponse:
    """Create a new group"""
    return schema.users.CreateGroupResponse(response=group.data)
