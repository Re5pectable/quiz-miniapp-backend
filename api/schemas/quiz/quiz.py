from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ... import db
from . import repository


class QuizCreate(BaseModel, db.RepositoryMixin):
    header: str
    short_name: str | None
    text: str
    config: dict | None
    point_keys: list[str] | None

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizOrm


class QuizEdit(QuizCreate):
    id: UUID
    is_active: bool


class QuizView(QuizEdit):
    created_at: datetime | None
    updated_at: datetime | None
    logo_url: str | None
    
    async def get_questions_amount(self) -> int:
        return await repository.get_quiz_questions_amount(self.id)


class QuizPreview(BaseModel, db.RepositoryMixin):
    id: UUID
    header: str
    logo_url: str | None
    
    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizOrm
    
