from fastapi import APIRouter, Request
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from app.config import settings
from app.supabase import supabase
import qrcode
import io
import uuid
from datetime import datetime


BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = APIRouter()

# --- Telegram handlers (v3 syntax) ---
tg_router = Router()


async def register_user_if_needed(telegram_id: int, username: str = None):
    """Register user in DB if they don't exist"""
    try:
        existing = (
            supabase.table("telegram_users")
            .select("unique_id")
            .eq("telegram_id", telegram_id)
            .maybe_single()
            .execute()
        )
        
        if existing.data is not None:
            return existing.data.get("unique_id")
    except Exception:
        pass
    
    # User doesn't exist, create new one
    unique_id = str(uuid.uuid4())
    try:
        supabase.table("telegram_users").insert({
            "telegram_id": telegram_id,
            "username": username,
            "unique_id": unique_id,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        # If table doesn't exist, just return the unique_id
        # The table will need to be created manually in Supabase
        pass
    return unique_id


@tg_router.message(Command("start"))
async def start_handler(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    
    unique_id = await register_user_if_needed(telegram_id, username)
    
    greeting = (
        f"👋 Welcome to Q-Loyal, {message.from_user.first_name}!\n\n"
        f"Your unique ID: `{unique_id}`\n\n"
        f"Use /help to see available commands."
    )
    await message.answer(greeting, parse_mode="Markdown")


@tg_router.message(Command("create_qr"))
async def create_qr_handler(message: types.Message):
    telegram_id = message.from_user.id
    
    # Get user's unique_id
    try:
        user = (
            supabase.table("telegram_users")
            .select("unique_id")
            .eq("telegram_id", telegram_id)
            .maybe_single()
            .execute()
        )
    except Exception:
        user = None
    
    if user is None or user.data is None:
        await message.answer("❌ User not found. Please use /start first.")
        return
    
    unique_id = user.data["unique_id"]
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(unique_id)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    
    # Send QR code
    await message.answer_photo(
        photo=types.BufferedInputFile(img_bytes.getvalue(), filename="qr_code.png"),
        caption=f"📱 Your Q-Loyal QR Code\n\nID: `{unique_id}`",
        parse_mode="Markdown"
    )


@tg_router.message(Command("clear_history"))
async def clear_history_handler(message: types.Message):
    telegram_id = message.from_user.id
    
    # Get user's unique_id
    try:
        user = (
            supabase.table("telegram_users")
            .select("unique_id")
            .eq("telegram_id", telegram_id)
            .maybe_single()
            .execute()
        )
    except Exception:
        user = None
    
    if user is None or user.data is None:
        await message.answer("❌ User not found. Please use /start first.")
        return
    
    unique_id = user.data["unique_id"]
    
    # Delete all stamps/visits for this user
    try:
        supabase.table("stamps").delete().eq("unique_id", unique_id).execute()
    except Exception:
        pass
    
    await message.answer("✅ Your stamp history has been cleared!")


@tg_router.message(Command("help"))
async def help_handler(message: types.Message):
    help_text = (
        "📋 **Available Commands:**\n\n"
        "/start - Greet and register in the system\n"
        "/create_qr - Generate your unique QR code\n"
        "/clear_history - Wipe your stamp/visit history\n"
        "/help - Show this help message"
    )
    await message.answer(help_text, parse_mode="Markdown")


dp.include_router(tg_router)

# --- FastAPI webhook endpoint ---
@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
