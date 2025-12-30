from app.database.models import async_session
from app.database.models import User, Bussines, Staff, Program, Card
from sqlalchemy import select

import secrets
from qr_comands import generate_qr

async def set_user(tg_id, username, language_code):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            qr_token = secrets.token_urlsafe(16)

            session.add(User(tg_id=tg_id, username=username, language_code=language_code, qr_token=qr_token))
            await session.commit()

async def generate_user_qr(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            qr = generate_qr(user.qr_token)
            return qr
            
        return None