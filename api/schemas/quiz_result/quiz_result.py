from datetime import datetime
from uuid import UUID
import json
from typing import Any


from fastapi import UploadFile
from pydantic import BaseModel, model_validator

from ... import db
from . import repository
from ...adapters import s3


class QuizResultCreate(BaseModel, db.RepositoryMixin):
    quiz_id: UUID
    header: str
    text: str
    points: dict[str, dict] | list[int]
    pic_url: str | None = None

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizResultOrm
        
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    async def create(self, picture: UploadFile | None):
        orm = await repository.create(**self.model_dump())
        if picture:
            extention = picture.filename.split(".")[-1]
            file_path = f"question_answers_pics/{orm.id}.{extention}"
            url = await s3.upload_file(picture.file, file_path)
            await self.db_update_fields_by_id(orm.id, pic_url=url)


class QuizResultEdit(QuizResultCreate):
    id: UUID
    
    async def update(self, picture: UploadFile | None = None):
        if picture:
            extention = picture.filename.split(".")[-1]
            file_path = f"quiz_results_pics/{self.id}.{extention}"
            url = await s3.upload_file(picture.file, file_path)
            self.pic_url = url
        await repository.update_(**self.model_dump())


class QuizResultView(QuizResultEdit):
    created_at: datetime
    updated_at: datetime | None
