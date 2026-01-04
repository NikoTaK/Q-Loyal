from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from app.strings_customer import get_text

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Help")],
        [KeyboardButton(text="QR Code")],
    ],
    resize_keyboard=True
)

def main_customer_kb(lang):
    webapp_url = "https://q-loyal.web.app" 
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("open_app", lang), web_app=WebAppInfo(url=webapp_url))],
            [KeyboardButton(text=get_text("my_qr", lang))]
        ],
        resize_keyboard=True
    )