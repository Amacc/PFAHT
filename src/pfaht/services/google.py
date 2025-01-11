from fastapi import Depends, Request, Cookie
from fastapi.responses import RedirectResponse
from typing import Annotated
import httpx
from .. import config, schema, db

token_url = "https://accounts.google.com/o/oauth2/token"


async def get_google_auth_token(
    request: Request,
    code: str,
    db: db.Database = Depends(db.get_database),
):
    """Returns the token response from Google for a given code."""
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

    # Now that we have the token, let's get the user info and store it in the database
    user_info = current_user()(request, google_json_response["access_token"])
    if user_info is None:
        return schema.auth.GetAuthGoogleResponse(
            message="Failed to get user info",
        )

    # Check if the user already exists
    user = schema.users.User.model_validate(user_info)
    query = "SELECT * FROM users WHERE id = :id"
    existing_user = await db.fetch_one(query=query, values={"id": user.id})
    if existing_user is None:
        # Create the user
        query = (
            "INSERT INTO users ("
            " id, email, verified_email, name, given_name, family_name, picture) "
            "VALUES (:id, :email, :verified_email, :name, :given_name, :family_name, :picture)"
        )
        await db.execute(query=query, values=user.model_dump())

    return google_json_response


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
