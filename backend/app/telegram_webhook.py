from fastapi import APIRouter, Request
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from app.config import settings



BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = APIRouter()

# --- Telegram handlers (v3 syntax) ---
tg_router = Router()

@tg_router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome to Q-Loyal!")

dp.include_router(tg_router)

# --- FastAPI webhook endpoint ---
@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
