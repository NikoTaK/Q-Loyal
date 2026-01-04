from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile


import app.keyboards as kb
import app.database.requests as rq

from qr_comands import generate_qr

from app.strings_customer import get_text


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    lang = message.from_user.language_code

    user = await rq.set_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        language_code=message.from_user.language_code
    )

    text = get_text("welcome", lang, name=message.from_user.first_name)
    await message.answer(text, reply_markup=kb.main_customer_kb(lang))

@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = message.from_user.language_code
    await message.answer(get_text("help", lang))

@router.message(Command("qr"))
@router.message(lambda message: "QR" in message.text)
async def cmd_qr(message: Message, bot: Bot):
    user = await rq.get_user(message.from_user.id)
    lang = user.language_code if user else "en"
    
    if not user or not user.qr_token:
        await message.answer(get_text("user_not_found", lang))
        return

    bot_info = await bot.get_me()
    qr_bytes_io = generate_qr(user.qr_token, bot_info.username)
    
    photo = BufferedInputFile(qr_bytes_io.getvalue(), filename="qr.png")
    await message.answer_photo(
        photo=photo, 
        caption=get_text("qr_caption", lang)
    )