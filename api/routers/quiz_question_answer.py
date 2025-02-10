from uuid import UUID
from fastapi import APIRouter, Body, Query, Depends, Response
from ..schemas.quiz_question_answer import QuizQuestionAnswerView, QuizQuestionAnswerEdit, QuizQuestionAnswerCreate
from .auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_question_answers(
    quiz_question_id: UUID = Query(),
):
    return await QuizQuestionAnswerView.get_many(quiz_question_id=quiz_question_id, is_deleted=False)


@router.get("/one")
async def get_quiz_question_answers_one(
    quiz_question_answer_id: UUID = Query(),
):
    return await QuizQuestionAnswerView.db_get_or_none(id=quiz_question_answer_id, is_deleted=False)


@router.post("")
async def create_quiz_question_answer(
    quiz_question_answer: QuizQuestionAnswerCreate,
    _: bool = Depends(authorized),
):
    await quiz_question_answer.create()


@router.put("")
async def update_quiz_question_answer(
    quiz_question_answer: QuizQuestionAnswerEdit,
    _: bool = Depends(authorized),
    
):
    await quiz_question_answer.update()
    return Response(headers={
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires" :"0",
    })


@router.delete("")
async def delete_quiz_question_answer(
    id: UUID = Body(embed=True),
    _: bool = Depends(authorized),
):
    await QuizQuestionAnswerView.db_update_fields_by_id(id, is_deleted=True)
