from sqlalchemy import select, update

from ... import db


async def __verify_points(session, **data):
    quiz_id = data['quiz__id']
    stmt = select(db.QuizOrm.point_fields).where(db.QuizOrm.id == quiz_id)
    q = await session.execute(stmt)
    point_fields = q.scalars().first()
    
    if any([True for point_name in data['points'].keys() if point_name not in point_fields]):
        raise ValueError("`points` keys should all be present in parent quiz `point_fields` field.")
    
async def create(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        obj = db.QuizResultOrm(**data)
        session.add(obj)
        await session.commit()
        
async def update_(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        id = data.pop('id')
        stmt = update(db.QuizResultOrm).values(**data).filter_by(id=id)
        await session.execute(stmt)
        await session.commit()