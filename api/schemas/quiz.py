from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from ..db import RepositoryMixin


class QuizCreate(BaseModel, RepositoryMixin):
    name: str
    short_name: str
    description: str


class QuizEdit(QuizCreate):
    pass


class QuizView(QuizCreate):
    id: UUID
    updated_at: datetime
    created_at: datetime
    logo_path: str

