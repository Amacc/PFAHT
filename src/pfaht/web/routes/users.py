from fastapi import Response, APIRouter, Depends
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


# @router.get("", response_model=schema.users.UserListResponse)
