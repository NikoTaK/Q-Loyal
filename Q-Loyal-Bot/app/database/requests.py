from app.database.models import async_session
from app.database.models import User, Bussines, Staff, Program, Card
from sqlalchemy import select

import secrets

async def set_user(tg_id, username, full_name, language_code):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            # Если юзера нет, создаем его с уникальным токеном
            new_user = User(
                tg_id=tg_id,
                username=username,
                full_name=full_name,
                language_code=language_code,
                qr_token=secrets.token_urlsafe(16) # Генерируем токен для QR
            )
            session.add(new_user)
            await session.commit()
            return new_user
        
        return user

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))