from uuid import UUID
from fastapi import APIRouter, Body, Query, File, UploadFile, Form
from ..schemas.quiz import QuizCreate, QuizEdit, QuizView, QuizPreview
from ._auth import authorized

router = APIRouter()


@router.get("")
async def get_quiz(id: UUID = Query()):
    return await QuizView.db_get_or_none(id=id, is_deleted=False)


@router.get("/all")
async def get_quize_previews():
    return await QuizPreview.db_get_many(is_deleted=False, is_active=True)


@router.post("")
async def create_quiz(
    _: authorized,
    quiz: QuizCreate = Form(),
    logo_pic: UploadFile = File(...),
):
    await quiz.db_create()


@router.put("")
async def update_quiz(
    _: authorized,
    data: QuizEdit = Body(...),
    logo_pic: UploadFile | None = File(None),
):
    await data.update(logo_pic=logo_pic)


@router.delete("")
async def delete_quiz(
    _: authorized,
    id: UUID = Body(embed=True),
):
    await QuizView.db_update_fields_by_id(id, is_deleted=True)
