from fastapi import HTTPException
from sqlalchemy import select, update

from ... import db


async def __verify_points(session, **data):
    quiz_id = data['quiz_id']
    stmt = select(db.QuizOrm.id, db.QuizOrm.point_keys).where(db.QuizOrm.id == quiz_id)
    q = await session.execute(stmt)
    quiz_id, point_keys = q.fetchone()
    
    if not quiz_id:
        raise HTTPException(404, "Quiz not found.")
    
    if not point_keys and not isinstance(data['points'], list):
        raise HTTPException(422, "If you don't use `point_keys`, `points` should be passed in numeric format.")
    
    if point_keys and any([True for point_name in data['points'].keys() if point_name not in point_keys]):
        raise HTTPException(422, "`points` keys should all be present in parent quiz `point_keys` field.")
    
async def create(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        obj = db.QuizResultOrm(**data)
        session.add(obj)
        await session.commit()
        return obj
        
async def update_(**data):
    async with db.Session() as session:
        await __verify_points(session, **data)
        id = data.pop('id')
        stmt = update(db.QuizResultOrm).values(**data).filter_by(id=id)
        await session.execute(stmt)
        await session.commit()