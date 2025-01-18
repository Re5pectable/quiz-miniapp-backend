from sqlalchemy import select

from ... import db


async def get_many(**kwargs) -> list[db.QuizQuestionOrm]:
    async with db.Session() as session:
        stmt = select(db.QuizQuestionOrm).filter_by(**kwargs).order_by(db.QuizQuestionOrm.order.asc())
        q = await session.execute(stmt)
        return q.scalars().all()
