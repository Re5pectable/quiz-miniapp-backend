from uuid import UUID
from fastapi import APIRouter
from ..schemas.game import Game

router = APIRouter()

@router.get("/{invitation_id}")
async def get_share_page(
    invitation_id: str
):
    return await Game.get_share(invitation_id)
