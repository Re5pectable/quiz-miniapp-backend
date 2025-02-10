from uuid import UUID
from fastapi import APIRouter, Body, Query, Depends, Form, UploadFile, File
from ..schemas.quiz_result import QuizResultCreate, QuizResultEdit, QuizResultView
from .auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz_results(
    quiz_id: UUID = Query(),
    _: bool = Depends(authorized),
):
    return await QuizResultView.db_get_many(quiz_id=quiz_id, is_deleted=False)

@router.get("/one")
async def get_quiz_results_one(
    quiz_result_id: UUID = Query(),
    _: bool = Depends(authorized),
):
    return await QuizResultView.db_get_or_none(id=quiz_result_id, is_deleted=False)


@router.post("")
async def create_quiz_result(
    quiz_result: QuizResultCreate = Form(),
    logo_pic: UploadFile | None = File(None),
    _: bool = Depends(authorized),
):
    await quiz_result.create(logo_pic)


@router.put("")
async def update_quiz_result(
    quiz_result: QuizResultEdit = Form(),
    logo_pic: UploadFile | None = File(None),
    _: bool = Depends(authorized),
):
    await quiz_result.update(logo_pic)


@router.delete("")
async def delete_quiz_result(
    id: UUID = Body(embed=True),
    _: bool = Depends(authorized),
):
    await QuizResultView.db_update_fields_by_id(id, is_deleted=True)
