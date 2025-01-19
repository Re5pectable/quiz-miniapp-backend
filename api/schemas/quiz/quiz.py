from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ... import db


class QuizCreate(BaseModel, db.RepositoryMixin):
    header: str
    short_name: str
    text: str
    config: dict
    point_fields: list[str]

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
    

class QuizPreview(BaseModel, db.RepositoryMixin):
    id: UUID
    header: str
    logo_url: str | None
    
    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizOrm
    
