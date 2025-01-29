from uuid import UUID

from fastapi import APIRouter, Body, Request

from ..schemas.sesssion import Session
from ._auth import authorized

router = APIRouter()

@router.post("/init")
async def init_session(
    request: Request,
    user_data: dict | None = Body({}),
    session_id: UUID | None = Body(None),
):
    return await Session.init(session_id, user_data, request)


@router.post("/try-auth")
async def login(
    request: Request,
    authorized: authorized,
):
    pass