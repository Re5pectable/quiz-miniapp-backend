from uuid import UUID
from fastapi import APIRouter, Body, Query
from ...schemas.quiz_question_answer import QuizQuestionAnswerView, QuizQuestionAnswerEdit, QuizQuestionAnswerCreate
from ._auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_question_answers(
    _: authorized,
    quiz_question_id: UUID = Query(),
):
    return await QuizQuestionAnswerView.get_many(quiz_question_id=quiz_question_id, is_deleted=False)


@router.post("")
async def create_quiz_question_answer(
    _: authorized,
    quiz_question_answer: QuizQuestionAnswerCreate,
):
    await quiz_question_answer.create()


@router.put("")
async def update_quiz_question_answer(
    _: authorized,
    quiz_question_answer: QuizQuestionAnswerEdit,
    
):
    await quiz_question_answer.update()


@router.delete("")
async def delete_quiz_question_answer(
    _: authorized,
    id: UUID = Body(embed=True),
):
    await QuizQuestionAnswerView.db_update_fields_by_id(id, is_deleted=True)
