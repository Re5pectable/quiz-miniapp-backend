from uuid import UUID

from pydantic import BaseModel
from fastapi import Request

from . import repository

class Session(BaseModel):
    
    id: UUID
    tg_id: str
    username: str
    
    @classmethod
    async def init(cls, id, user_data, request: Request) -> UUID:
        return await repository.init_session(id, user_data, request.headers.get("user-agent"))
