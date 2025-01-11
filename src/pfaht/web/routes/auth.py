from logging import getLogger
from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter, Request, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
import httpx
from jose import jwt

# from jose import jwt
from urllib import parse
from ... import config, schema, services

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
async def auth_google(
    response: Response,
    token_response: dict = Depends(services.google.get_google_auth_token),
):
    logger.debug(f"{token_response=}")
    for google_json_key, google_json_value in token_response.items():
        response.set_cookie(
            google_json_key,
            google_json_value,
            httponly=True,
            samesite="strict",
        )
    return schema.auth.GetAuthGoogleResponse(
        message="Successfully authenticated with Google",
    )


@router.get("/google/token")
async def get_token(access_token: Annotated[str | None, Cookie()] = None):
    return jwt.decode(access_token, config.GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


@router.get("/google/me")
async def google_me(user=Depends(services.google.current_user())):
    return schema.auth.GetGoogleMeResponse(response=user)
