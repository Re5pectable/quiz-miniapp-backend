from sqlalchemy import func, select

from ... import db


async def get_quiz_questions_amount(quiz_id) -> tuple[db.QuizOrm, int]:
    async with db.Session() as session:
        stmt = (
            select(func.count())
            .select_from(db.QuizQuestionOrm)
            .where(
                db.QuizQuestionOrm.quiz_id == quiz_id,
                db.QuizQuestionOrm.is_deleted.is_not(True),
            )
        )
        q = await session.execute(stmt)
        return q.scalars().first()
