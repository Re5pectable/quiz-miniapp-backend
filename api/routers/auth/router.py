import secrets
from uuid import uuid4

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ...config import DEBUG, api_config
from .auth import CredentialsException
from .token import AccessToken, RefreshToken

router = APIRouter()


@router.post("")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    given_username_b, correct_username_b = form_data.username.encode("utf8"), api_config.login.encode("utf8")
    given_password_b, correct_password_b = form_data.password.encode("utf8"), api_config.password.encode("utf8")

    if not (
        secrets.compare_digest(given_username_b, correct_username_b)
        and secrets.compare_digest(given_password_b, correct_password_b)
    ):
        raise HTTPException(404)
    
    data = dict(token_id=str(uuid4()))
    access_token = AccessToken.new(data)
    refresh_token = RefreshToken.new(data)

    response = JSONResponse({"access_token": access_token.to_jwt}, status_code=201)
    response.set_cookie(
        key="refresh_token",
        expires=refresh_token.expires,
        value=refresh_token.to_jwt,
        samesite='lax',
        httponly=True,
        secure=True if not DEBUG else False,
    )
    return response


@router.post("/new-access-token")
async def new_access_token(
    refresh_token: str = Cookie(None),
):
    if not refresh_token:
        raise HTTPException(403)
    _ = RefreshToken.from_jwt(refresh_token)
    new_access_token = AccessToken.new({})
    return JSONResponse({"access_token": new_access_token.to_jwt}, status_code=200)
