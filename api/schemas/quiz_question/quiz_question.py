from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, TypeAdapter

from ... import db
from . import repository


class QuizQuestionCreate(BaseModel, db.RepositoryMixin):

    quiz_id: UUID
    text: str
    pic_url: str | None
    order: int

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizQuestionOrm


class QuizQuestionEdit(QuizQuestionCreate):
    id: UUID


class QuizQuestionView(QuizQuestionEdit):
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    async def get_many(cls, **kwargs):
        data = await repository.get_many(**kwargs)
        return TypeAdapter(list[cls]).validate_python(data)
