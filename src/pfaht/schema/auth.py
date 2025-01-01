from pydantic import BaseModel
from . import api, users


class GetAuthLoginResponse(api.ApiResponse[None]):
    pass


class GoogleAuthResponse(BaseModel):
    access_tooken: str
    expires_in: int
    refresh_token: str


class GetAuthGoogleResponse(api.ApiResponse[None]):
    pass


class GetGoogleMeResponse(api.ApiResponse[users.User | None]):

    def model_post_init(self, __context):
        super().model_post_init(__context)
        if isinstance(self.response, users.User):
            self.links.update(ProfileImage=self.response.picture)
