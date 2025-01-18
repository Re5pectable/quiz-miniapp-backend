from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, TypeAdapter

from ... import db
from . import repository


class QuizQuestionAnswerCreate(BaseModel, db.RepositoryMixin):
    quiz_question_id: UUID
    text: str
    note: str | None
    points: dict
    order: int

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizQuestionAnswerOrm
        
    async def create(self):
        await repository.create(**self.model_dump())


class QuizQuestionAnswerEdit(QuizQuestionAnswerCreate):
    id: UUID
        
    async def update(self):
        await repository.update_(**self.model_dump())


class QuizQuestionAnswerView(QuizQuestionAnswerEdit):
    created_at: datetime | None
    updated_at: datetime | None
    
    @classmethod
    async def get_many(cls, **kwargs):
        data = await repository.get_many(**kwargs)
        return TypeAdapter(list[cls]).validate_python(data)
