from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ... import db
from . import repository


class QuizResultCreate(BaseModel, db.RepositoryMixin):
    quiz_id: UUID
    header: str
    text: str
    points: dict[str, dict]
    pic_url: str | None

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizResultOrm
    
    async def create(self):
        await repository.create(**self.model_dump())


class QuizResultEdit(QuizResultCreate):
    id: UUID
    
    async def update(self):
        await repository.update_(**self.model_dump())


class QuizResultView(QuizResultEdit):
    created_at: datetime
    updated_at: datetime | None
