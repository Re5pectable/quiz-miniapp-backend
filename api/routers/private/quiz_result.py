from uuid import UUID
from fastapi import APIRouter, Body, Query
from ...schemas.quiz_result import QuizResultCreate, QuizResultEdit, QuizResultView
from ._auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_results(
    _: authorized,
    quiz_id: UUID = Query(),
):
    return await QuizResultView.db_get_many(quiz_id=quiz_id, is_deleted=False)


@router.post("")
async def create_quiz_result(
    _: authorized,
    quiz_result: QuizResultCreate,
):
    await quiz_result.create()


@router.put("")
async def update_quiz_result(
    _: authorized,
    quiz_result: QuizResultEdit,
    
):
    await quiz_result.update()


@router.delete("")
async def delete_quiz_result(
    _: authorized,
    id: UUID = Body(embed=True),
):
    await QuizResultView.db_update_fields_by_id(id, is_deleted=True)
