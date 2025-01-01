from logging import getLogger
from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter, Request, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
import httpx
from jose import jwt

# from jose import jwt
from urllib import parse
from ... import config, schema

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = getLogger(__name__)


@router.get("/login")
async def login(request: Request):
    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "access_type": "offline",
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
    }
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?{parse.urlencode(params)}"
    )
    return RedirectResponse(google_auth_url)


@router.get("/google")
async def auth_google(code: str, response: Response):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    google_response = httpx.post(token_url, data=data)
    try:
        google_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return schema.auth.GetAuthGoogleResponse(
            message=f"Failed to get token: {e}",
        )
    google_json_response = google_response.json()
    # TODO: Update to generate a proper session token
    logger.debug(f"{google_json_response=}")
    for google_json_key, google_json_value in google_json_response.items():
        response.set_cookie(
            google_json_key,
            google_json_value,
            httponly=True,
            samesite="strict",
        )
    return schema.auth.GetAuthGoogleResponse(
        message="Successfully authenticated with Google",
    )


def current_user(redirect_on_fail: bool = False):
    """Get the current user data

    Args:
        redirect_on_fail (bool, optional): Redirect to login page on fail. Defaults to False.
    """

    def _internal(
        request: Request,
        access_token: Annotated[str | None, Cookie()] = None,
    ):
        """Function to get the current user data"""
        user_info = httpx.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        try:
            user_info.raise_for_status()
        except httpx.HTTPStatusError as e:
            if redirect_on_fail:
                # will raise w/ proper exception to redirect response later
                return RedirectResponse("/auth/login")
            return None
        user = schema.users.User.model_validate(user_info.json())
        # Assign the user to the request state for use in templates
        request.state.user = user
        return user

    return _internal


@router.get("/google/token")
async def get_token(access_token: Annotated[str | None, Cookie()] = None):
    return jwt.decode(access_token, config.GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


@router.get("/google/me")
async def google_me(user=Depends(current_user())):
    return schema.auth.GetGoogleMeResponse(response=user)
