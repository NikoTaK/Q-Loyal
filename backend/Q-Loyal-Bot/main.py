from config import API_TOKEN
from qr_comands import decode_qr, generate_qr
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import sqlite3
import os

def get_user(cursor, user_id):
    cursor.execute(
        "SELECT qr_path, role FROM tg_user WHERE id = ?;",
        (user_id,)
    )
    return cursor.fetchone()


bot = TeleBot(token=API_TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button = KeyboardButton(text="Create QR", request_contact=True)
keyboard.add(button)


with sqlite3.connect('tg_user.db') as connection:
    cursor = connection.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS tg_user(
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            qr_path TEXT,
            role TEXT NOT NULL DEFAULT 'customer'
        );
    """
    cursor.execute(create_table_query)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Welcome to the bot", reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    user_id = message.contact.user_id

    with sqlite3.connect('tg_user.db') as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT qr_path FROM tg_user WHERE id = ?;",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            qr_path = result[0]
        else:
            qr_path = generate_qr(user_id)

            insert_query = """
                INSERT INTO tg_user(id, first_name, last_name, phone_number, qr_path)
                VALUES(?, ?, ?, ?, ?);
            """
            data = ( 
            user_id,
            f'{message.contact.first_name}',
            f'{message.contact.last_name}',
            f'{message.contact.phone_number}',
            f'{qr_path}'
            )
            cursor.execute(insert_query, data)

    bot.send_message(message.chat.id, "✅ Your personal QR code is ready")
    bot.send_photo(message.chat.id, open(qr_path, 'rb'))


@bot.message_handler(commands=['my_qr'])
def my_qr(message):
    user_id = message.from_user.id

    with sqlite3.connect('tg_user.db') as connection:
        cursor = connection.cursor()
        user = get_user(cursor, user_id)

    if not user:
        bot.send_message(
            message.chat.id,
            "❗ To create your QR, please share your contact first.",
            reply_markup=keyboard
        )
        return
    else:
        qr_path = user[0]
        bot.send_photo(message.chat.id, open(qr_path, 'rb'))


@bot.message_handler(commands=['become_merchant'])
def become_merchant(message):
    user_id = message.from_user.id

    with sqlite3.connect('tg_user.db') as connection:
        cursor = connection.cursor()
        user = get_user(cursor, user_id)

        if not user:
            bot.send_message(
                message.chat.id,
                "❗ Please create your user profile first by sharing your contact.",
                reply_markup=keyboard
            )
            return
        else:
            cursor.execute(
                "UPDATE tg_user SET role = 'merchant' WHERE id = ?;",
                (user_id,)
            )
            bot.send_message(
                message.chat.id,
                "✅ You are now registered as a merchant.\nYou can scan customer QR codes."
            )


@bot.message_handler(commands=['scan_qr'])
def scan_qr(message):
    user_id = message.from_user.id

    with sqlite3.connect('tg_user.db') as connection:
        cursor = connection.cursor()
        user = get_user(cursor, user_id)

    if not user:
        bot.send_message(
            message.chat.id,
            "❗ Please create your profile first by sharing your contact.",
            reply_markup=keyboard
        )
        return

    role = user[1]

    if role != 'merchant':
        bot.send_message(
            message.chat.id,
            "⛔ This action is only available for merchants."
        )
        return

    bot.send_message(
        message.chat.id,
        "📷 Please send a photo of the customer’s QR code."
    )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id

    with sqlite3.connect('tg_user.db') as connection:
        cursor = connection.cursor()
        user = get_user(cursor, user_id)

    if not user:
        bot.send_message(
            message.chat.id,
            "❗ Please create your profile first by sharing your contact.",
            reply_markup=keyboard
        )
        return

    role = user[1]

    if role != 'merchant':
        bot.send_message(
            message.chat.id,
            "⛔ Only merchants can scan QR codes.\nIf you are a merchant, use /become_merchant."
        )
        return

    else:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        os.makedirs("scans", exist_ok=True)
        scan_path = f"scans/{file_id}.jpg"

        with open(scan_path, "wb") as f:
            f.write(downloaded_file)

        decoded_text = decode_qr(scan_path)

        if not decoded_text or not decoded_text.startswith("tg_user:"):
            bot.send_message(
                message.chat.id,
                "❌ Could not detect a valid QR code."
            )
            return
        
        scanned_user_id = int(decoded_text.split(":")[1])

        # merchant_id = message.from_user.id

        # if scanned_user_id == merchant_id:
        #     bot.send_message(
        #         message.chat.id,
        #         "⛔ You cannot scan your own QR code."
        #     )
        #     return

        scanned_user = get_user(cursor, scanned_user_id)
        if not scanned_user:
            bot.send_message(
                message.chat.id,
                "❌ This QR code does not belong to a registered user."
            )
            return
        else:
            bot.send_message(
                message.chat.id,
                f"✅ QR scanned successfully\nUser ID: {scanned_user_id}"
            )


bot.polling()

