from pydantic import BaseModel
from . import api, services


class User(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str


class NewGroup(BaseModel):
    name: str


class Group(NewGroup):
    id: int


class UserGroup(BaseModel):
    user_id: str
    group_id: str


class GetUserResponse(api.ApiResponse[User]):
    pass


class ListUserResponse(api.PagedApiResponse[User]):
    pass


class CreateGroupResponse(api.ApiResponse[Group]):
    pass


class DeleteUserResponse(api.ApiResponse[bool]):
    pass


class ListGroupResponse(api.PagedApiResponse[Group]):
    pass


class GroupServiceResponse(services.ServiceResponse[Group]):
    pass


class GroupListServiceResponse(services.ServiceResponseList[Group]):
    pass
