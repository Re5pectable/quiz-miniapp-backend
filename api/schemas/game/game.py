from uuid import UUID

from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from ... import db
from . import repository
from ..quiz import QuizView
from ...utils import result_to_png


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
    async def __get(cls, game_id: UUID):
        game = await cls.db_get_or_none(id=game_id)
        if not game:
            raise HTTPException(404, "Game not found.")
        return game

    @classmethod
    async def start(cls, quiz_id: UUID, session_id: UUID):
        game_id = await repository.create(quiz_id, session_id)
        return {"game_id": game_id}

    @classmethod
    async def get_info(cls, game_id: UUID):
        game = await cls.__get(game_id)
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
        game = await cls.__get(game_id)
        if game.is_finished:
            return {"is_finished": True}

        question, answers = await repository.get_question(game.current_quiz_question_id)
        return {
            "question": question,
            "answers": answers,
        }
    
    @classmethod
    async def get_result(cls, game_id: UUID):
        game = await cls.__get(game_id)
        if not game.is_finished:
            raise HTTPException(403, "This quiz has not been finished yet.")
        result, copy, invitation_id = await repository.get_or_generate_result(game.id)
        return {
            "copy": copy,
            "header": result.header,
            "text": result.text,
            "pic_url": result.pic_url,
            "points": result.points,
            "invitation_id": invitation_id,
        }
        

    @classmethod
    async def make_answer(cls, game_id: UUID, answer_id: UUID):
        game = await cls.__get(game_id)
        if game.is_finished:
            raise HTTPException(400, "Game is finished.")
        chosen, correct = await repository.make_answer(
            game_id, game.current_quiz_question_id, answer_id
        )
        success = chosen.id == correct.id
        return {
            "correct": success,
            "chosen_note": chosen.note,
            "correct_id": correct.id,
        }

    @classmethod
    async def get_share(cls, invitation_id):
        quiz, game, result, invitation = await repository.get_share(invitation_id)
        
        image_url = invitation.image_url
        if not image_url:
            image_url = await result_to_png.make(
                quiz.logo_url,
                game.result['points'],
                game.result['total_questions']
            )
            await repository.update_invitation(invitation_id, image_url=image_url)
        
        html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta property="og:title" content="{quiz.header}" />
                <meta property="og:site_name" content="Клей Тесты">
                <meta property="og:description" content="{result.text}" />
                <meta property="og:image" content="{image_url}" />
                <meta property="og:type" content="website" />
                <meta property="og:url" content="https://t.me/KleyMediaBot/Quiz?startapp={quiz.id}"/>
                
                <meta name="twitter:card" content="summary_large_image">
                <meta name="twitter:image" content="{image_url}">
            </head>
            <body>
                <script>
                    window.location.href = "https://t.me/KleyMediaBot/Quiz?startapp={quiz.id}"
                </script>
            </body>
            </html>
        """
        return HTMLResponse(html_content)
        