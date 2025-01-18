from uuid import UUID

from fastapi import APIRouter, Body, Query

from ...schemas.quiz_question import (
    QuizQuestionCreate,
    QuizQuestionEdit,
    QuizQuestionView,
)
from ._auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_questions(
    _: authorized,
    quiz_id: UUID = Query(),
):
    return await QuizQuestionView.get_many(quiz_id=quiz_id, is_deleted=False)


@router.post("")
async def create_quiz_question(
    _: authorized,
    quiz_question: QuizQuestionCreate,
):
    await quiz_question.db_create()


@router.put("")
async def update_quiz_question(
    _: authorized,
    quiz_question: QuizQuestionEdit,
):
    await quiz_question.db_update()


@router.delete("")
async def delete_quiz_question(
    _: authorized,
    id: UUID = Body(embed=True),
):
    await QuizQuestionView.db_update_fields_by_id(id, is_deleted=True)
