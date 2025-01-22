from uuid import UUID

from pydantic import BaseModel
from fastapi import HTTPException

from ... import db
from . import repository
from ..quiz import QuizView


class Game(BaseModel, db.RepositoryMixin):
    id: UUID
    session_id: UUID
    quiz_id: UUID
    current_quiz_question_id: UUID | None
    quiz_result_id: UUID | None
    result: dict | None
    is_finished: bool | None

    class Config:
        from_attributes = True

    class Meta:
        orm_model = db.GameOrm

    @classmethod
    async def start(cls, quiz_id: UUID, session_id: UUID):
        game_id = await repository.create(quiz_id, session_id)
        return {"game_id": game_id}

    @classmethod
    async def get_info(cls, game_id: UUID):
        game = await cls.db_get_or_none(id=game_id)
        quiz = await QuizView.db_get_or_none(id=game.quiz_id)
        questions_count = await quiz.get_questions_amount()
        return {
            "quiz": {
                "id": quiz.id,
                "header": quiz.header,
                "logo_url": quiz.logo_url,
                "n_questions": questions_count,
            },
            "is_finished": game.is_finished,
        }

    @classmethod
    async def next(cls, game_id: UUID):
        game = await cls.db_get_or_none(id=game_id)
        if game.is_finished:
            return {"is_finished": True}

        question, answers = await repository.get_question(game.current_quiz_question_id)
        return {
            "question": question,
            "answers": answers,
        }
    
    @classmethod
    async def get_result(cls, game_id: UUID):
        game = await cls.db_get_or_none(id=game_id)
        if not game.is_finished:
            raise HTTPException(403, "This quiz has not been finished yet.")
        result, copy = await repository.get_or_generate_result(game.id)
        return {
            "copy": copy,
            "header": result.header,
            "text": result.text,
            "pic_url": result.pic_url,
            "points": result.points
        }
        

    @classmethod
    async def make_answer(cls, game_id: UUID, answer_id: UUID):
        game = await cls.db_get_or_none(id=game_id)
        chosen, correct = await repository.make_answer(
            game_id, game.current_quiz_question_id, answer_id
        )
        success = chosen.id == correct.id
        return {
            "correct": success,
            "chosen_note": chosen.note,
            "correct_id": correct.id,
        }
