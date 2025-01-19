from uuid import UUID
from fastapi import APIRouter, Body, Query
from ..schemas.quiz import QuizCreate, QuizEdit, QuizView
from ._auth import authorized

router = APIRouter()


@router.get("")
async def get_quizes(
    # _: authorized
):
    return await QuizView.db_get_many(is_deleted=False)

@router.get("")
async def get_quiz(
    # _: authorized
    id: UUID = Query()
):
    return await QuizView.db_get_or_none(id=id, is_deleted=False)


@router.post("")
async def create_quiz(
    _: authorized,
    quiz: QuizCreate,
):
    await quiz.db_create()


@router.put("")
async def update_quiz(
    _: authorized,
    data: QuizEdit,
):
    await data.db_update()


@router.delete("")
async def delete_quiz(
    _: authorized,
    id: UUID = Body(embed=True),
):
    await QuizView.db_update_fields_by_id(id, is_deleted=True)
