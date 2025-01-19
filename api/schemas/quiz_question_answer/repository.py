from sqlalchemy import select, update

from ... import db


async def __verify_points(session, **data):
    quiz_question_id = data['quiz_question_id']
    stmt = (
        select(db.QuizOrm.point_fields)
        .select_from(db.QuizOrm)
        .join(db.QuizQuestionOrm, db.QuizQuestionOrm.quiz_id == db.QuizOrm.id)
        .where(db.QuizQuestionOrm.id == quiz_question_id)
    )
    q = await session.execute(stmt)
    point_fields = q.scalars().first()
    
    if point_fields is None:
        raise ValueError("quiz not found.")
    
    if any([True for point_name in data['points'].keys() if point_name not in point_fields]):
        raise ValueError("`points` keys should all be present in parent quiz `point_fields` field.")

async def get_many(**kwargs) -> list[db.QuizQuestionAnswerOrm]:
    async with db.Session() as session:
        stmt = select(db.QuizQuestionAnswerOrm).filter_by(**kwargs).order_by(db.QuizQuestionAnswerOrm.order.asc())
        q = await session.execute(stmt)
        return q.scalars().all()


async def create(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        obj = db.QuizQuestionAnswerOrm(**data)
        session.add(obj)
        await session.commit()
        
async def update_(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        id = data.pop('id')
        stmt = update(db.QuizQuestionAnswerOrm).values(**data).filter_by(id=id)
        await session.execute(stmt)
        await session.commit()
