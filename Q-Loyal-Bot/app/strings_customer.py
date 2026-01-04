STRINGS = {
    "ru": {
        "welcome": "Привет, {name}! 👋\n\nДобро пожаловать в Q-Loyal. Копите штампы и получайте подарки!",
        "open_app": "🎁 Открыть приложение",
        "my_qr": "📷 Мой QR-код",
        "qr_caption": "Ваш личный QR-код.\n\nПокажите его сотруднику заведения, чтобы получить штамп! ✨",
        "user_not_found": "Ошибка: пользователь не найден. Нажмите /start",
        "help": "Команды:\n/start - Регистрация\n/qr - Мой код\n/help - Помощь"
    },
    "en": {
        "welcome": "Hello, {name}! 👋\n\nWelcome to Q-Loyal. Collect stamps and get rewards!",
        "open_app": "🎁 Open App",
        "my_qr": "📷 My QR-code",
        "qr_caption": "Your personal QR code.\n\nShow it to the staff to get a stamp! ✨",
        "user_not_found": "Error: user not found. Press /start",
        "help": "Commands:\n/start - Registration\n/qr - My code\n/help - Help"
    },
    "uz": {
        "welcome": "Salom, {name}! 👋\n\nQ-Loyal ga xush kelibsiz. Stamp yig'ing va sovg'alarni qo'lga kiring!",
        "open_app": "🎁 Ilovani ochish",
        "my_qr": "📷 Mening QR-kodim",
        "qr_caption": "Sizning shaxsiy QR-kodingiz.\n\nStamp olish uchun ishchi bilan QR-kodni ko'rsating! ✨",
        "user_not_found": "Xatolik: foydalanuvchi topilmadi. /start tugmasini bosing",
        "help": "Buyruqlar:\n/start - Ro'yxatdan o'tish\n/qr - Mening kodim\n/help - Yordam"
    }
}

def get_text(key, lang, **kwargs):
    # Если языка нет в словаре, используем английский по умолчанию
    texts = STRINGS.get(lang, STRINGS["en"])
    text = texts.get(key, STRINGS["en"][key])
    return text.format(**kwargs)