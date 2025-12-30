from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
import app.database.requests as rq


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username, message.from_user.language_code)
    await message.answer("Hello! This is your bot.", reply_markup=kb.mini_app)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Available commands: /start, /help, /qr")

@router.message(Command("qr"))
async def cmd_qr(message: Message):
    result = await rq.generate_user_qr(message.from_user.id)
    if result:
        photo = BufferedInputFile(result.getvalue(), filename="qr-code.png")
        await message.answer_photo(photo=photo, caption="Here is your QR code!")
    else:
        await message.answer("Failed to generate QR code. Please try again later.")