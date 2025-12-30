from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Help")],
        [KeyboardButton(text="QR Code")],
    ],
    resize_keyboard=True
)

mini_app = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Q-Loyal Mini App", web_app=WebAppInfo(url="https://q-loyal.web.app"))],
    ]
)