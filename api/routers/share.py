from uuid import UUID
from fastapi import APIRouter
from ..schemas.game import Game

router = APIRouter()

@router.get("/{game_id}")
async def get_share_page(
    game_id: UUID
):
    return await Game.get_share(game_id)
