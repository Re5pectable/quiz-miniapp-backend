from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError

from .token import AccessToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token_str: str = Depends(oauth2_scheme)):
    try:
        AccessToken.from_jwt(token_str)
    except JWTError:
        raise CredentialsException()
    
    return True


async def authorized(__authenticated: bool = Depends(get_current_user)):
    return __authenticated
