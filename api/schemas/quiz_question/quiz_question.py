from datetime import datetime
from uuid import UUID
import json
from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel, TypeAdapter, model_validator

from ... import db
from ...adapters import s3
from . import repository


class QuizQuestionCreate(BaseModel, db.RepositoryMixin):

    quiz_id: UUID
    text: str
    order: int

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizQuestionOrm
        
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
        
    async def create(self, picture: UploadFile | None = None):
        orm = await self.db_create()
        if picture:
            extention = picture.filename.split(".")[-1]
            file_path = f"img/questions/{orm.id}.{extention}"
            url = await s3.upload_file(picture.file, file_path)
            await self.db_update_fields_by_id(orm.id, pic_url=url)
            


class QuizQuestionEdit(QuizQuestionCreate):
    id: UUID
    pic_url: str | None
    
    async def update(self, picture: UploadFile | None = None):
        if picture:
            extention = picture.filename.split(".")[-1]
            file_path = f"img/questions/{self.id}.{extention}"
            url = await s3.upload_file(picture.file, file_path)
            self.pic_url = url
            
        await self.db_update()


class QuizQuestionView(QuizQuestionEdit):
    created_at: datetime
    updated_at: datetime | None
    pic_url: str | None

    @classmethod
    async def get_many(cls, **kwargs):
        data = await repository.get_many(**kwargs)
        return TypeAdapter(list[cls]).validate_python(data)
