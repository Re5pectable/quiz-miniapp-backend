from datetime import datetime, timedelta, timezone

from jose import jwt

from ...config import api_config


class JWTToken:
    claims: dict
    expires: datetime

    lifetime: timedelta

    def __init__(self, claims: dict, expires: datetime):
        if not isinstance(claims, dict):
            raise ValueError("'claims' must be a dict")
        if not isinstance(expires, datetime):
            raise ValueError("'expires' must be a datetime")

        self.claims = claims
        self.expires = expires

    @classmethod
    def from_jwt(cls, token_str: str):
        decoded = jwt.decode(
            token_str, api_config.JWT_SECRET, algorithms=api_config.JWT_ALGO
        )
        expires = datetime.fromtimestamp(decoded["exp"])
        return cls(decoded, expires)

    @property
    def to_jwt(self) -> str:
        to_encode = self.claims | {"exp": self.exp}
        return jwt.encode(
            to_encode, api_config.JWT_SECRET, algorithm=api_config.JWT_ALGO
        )

    @property
    def exp(self) -> int:
        return int(self.expires.timestamp())


class ApiToken(JWTToken):

    lifetime: timedelta

    @classmethod
    def new(cls, claims: dict):
        return cls(claims, datetime.now(timezone(timedelta(hours=0))) + cls.lifetime)


class AccessToken(ApiToken):
    lifetime = timedelta(seconds=api_config.JWT_ACCESS_EXP_SEC)


class RefreshToken(ApiToken):
    lifetime = timedelta(seconds=api_config.JWT_REFRESH_EXP_SEC)
