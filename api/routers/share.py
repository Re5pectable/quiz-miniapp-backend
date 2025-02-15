from fastapi import APIRouter
from ..schemas.game import Game

router = APIRouter()

@router.get("/{entity_id}")
async def get_share_page(
    entity_id: str
):
    return await Game.get_share(entity_id)
