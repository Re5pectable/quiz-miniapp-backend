from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query

from ..schemas.game import Game
from .auth import get_session

router = APIRouter()

@router.post("/start")
async def start_game(
    quiz_id: UUID = Body(embed=True),
    session_id: UUID | None = Depends(get_session)
):
    return await Game.start(quiz_id, session_id)

@router.get("")
async def get_game(
    game_id: UUID = Query(),
):
    return await Game.get_info(game_id)

@router.get("/next")
async def get_next_page(
    game_id: UUID = Query(),
):
    return await Game.next(game_id)

@router.post("/answer")
async def answer(
    game_id: UUID = Body(),
    answer_id: UUID = Body(),
):
    return await Game.make_answer(game_id, answer_id)

@router.get("/result")
async def get_result(
    game_id: UUID = Query()
):
    return await Game.get_result(game_id)