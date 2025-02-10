from uuid import UUID

from fastapi import APIRouter, Body, Depends, File, Form, Query, UploadFile

from ..schemas.quiz import QuizCreate, QuizEdit, QuizPreview, QuizView
from .auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz(id: UUID = Query()):
    return await QuizView.db_get_or_none(id=id, is_deleted=False)


@router.get("/all")
async def get_quize_previews():
    return await QuizPreview.db_get_many(is_deleted=False, is_active=True)

@router.get("/all/admin")
async def get_quize_previews_all(
    _: bool = Depends(authorized),
):
    return await QuizPreview.db_get_many(is_deleted=False)


@router.post("")
async def create_quiz(
    quiz: QuizCreate = Form(),
    logo_pic: UploadFile = File(...),
    _: bool = Depends(authorized),
):
    await quiz.create(logo_pic)


@router.put("")
async def update_quiz(
    data: QuizEdit = Body(...),
    logo_pic: UploadFile | None = File(None),
    _: bool = Depends(authorized),
):
    await data.update(logo_pic=logo_pic)


@router.delete("")
async def delete_quiz(
    id: UUID = Body(embed=True),
    _: bool = Depends(authorized),
):
    await QuizView.db_update_fields_by_id(id, is_deleted=True)
