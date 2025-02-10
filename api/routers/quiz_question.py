from uuid import UUID

from fastapi import APIRouter, Body, Query, Depends, UploadFile, File, Form

from ..schemas.quiz_question import (
    QuizQuestionCreate,
    QuizQuestionEdit,
    QuizQuestionView,
)
from .auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_questions(
    quiz_id: UUID = Query(),
):
    return await QuizQuestionView.get_many(quiz_id=quiz_id, is_deleted=False)

@router.get("/one")
async def get_quiz_question(
    question_id: UUID = Query(),
):
    return await QuizQuestionView.db_get_or_none(id=question_id, is_deleted=False)

@router.post("")
async def create_quiz_question(
    quiz_question: QuizQuestionCreate = Form(),
    picture: UploadFile | None = File(None),
    _: bool = Depends(authorized),
):
    await quiz_question.create(picture=picture)


@router.put("")
async def update_quiz_question(
    quiz_question: QuizQuestionEdit = Form(),
    picture: UploadFile | None = File(None),
    _: bool = Depends(authorized),
):
    await quiz_question.update(picture=picture)


@router.delete("")
async def delete_quiz_question(
    id: UUID = Body(embed=True),
    _: bool = Depends(authorized),
):
    await QuizQuestionView.db_update_fields_by_id(id, is_deleted=True)
