from datetime import datetime
from uuid import UUID
from typing import Any
import json

from pydantic import BaseModel, model_validator
from fastapi import UploadFile

from ... import db
from . import repository
from ...adapters import s3
from ...utils import result_to_png


class QuizCreate(BaseModel, db.RepositoryMixin):
    category: str
    type: str
    header: str
    short_name: str | None
    text: str
    config: dict | None = None
    point_keys: list[str] | None
    logo_url: str | None = None

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizOrm
        
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    async def create(self, logo_pic: UploadFile):
        orm = await self.db_create()
        if logo_pic:
            extention = logo_pic.filename.split(".")[-1]
            file_path = f"img/quizes/{orm.id}.{extention}"
            url = await s3.upload_file(logo_pic.file, file_path)
            await self.db_update_fields_by_id(orm.id, logo_url = url)
            
            filebody = result_to_png.logo_to_og(url)
            file_path = f"img/quizes/{orm.id}_og.{extention}"
            url = await s3.upload_file(filebody, file_path)
            
            


class QuizEdit(QuizCreate):
    id: UUID
    category: str
    type: str
    is_active: bool
    
    async def update(self, logo_pic: UploadFile | None = None):
        if logo_pic:
            extention = logo_pic.filename.split(".")[-1]
            file_path = f"img/quizes/{self.id}.{extention}"
            url = await s3.upload_file(logo_pic.file, file_path)
            self.logo_url = url
            
            filebody = result_to_png.logo_to_og(url)
            file_path = f"img/quizes/{self.id}_og.{extention}"
            url = await s3.upload_file(filebody, file_path)
        await self.db_update()


class QuizView(QuizEdit):
    created_at: datetime | None
    updated_at: datetime | None
    logo_url: str | None
    
    async def get_questions_amount(self) -> int:
        return await repository.get_quiz_questions_amount(self.id)


class QuizPreview(BaseModel, db.RepositoryMixin):
    id: UUID
    created_at: datetime | None
    header: str
    category: str
    type: str
    logo_url: str | None
    is_active: bool
    
    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.QuizOrm
    
