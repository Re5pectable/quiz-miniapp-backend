from uuid import UUID

import user_agents
from sqlalchemy import select

from ... import db


def parse_user_agent(agent: str):
    agent = user_agents.parse(agent)
    return {
        'os': {"family": agent.os.family, "version": agent.os.version},
        'browser': {"family": agent.browser.family, "version": agent.browser.version},
        'device': {"family": agent.device.family, "brand": agent.device.brand},
    }


async def init_session(id, user_data: dict, user_agent) -> UUID:
    user_agent = parse_user_agent(user_agent)
    async with db.Session() as session:
        stmt = select(db.SessionOrm.id).filter_by(id=id)
        q = await session.execute(stmt)
        session_id = q.scalars().first()

        if session_id:
            return session_id
        
        tg_id = user_data.get("id")
        tg_id = str(tg_id) if tg_id is not None else None
        username = user_data.get("username")

        obj = db.SessionOrm(tg_id=tg_id, username=username, user_agent=user_agent)
        session.add(obj)
        await session.commit()
        return obj.id
