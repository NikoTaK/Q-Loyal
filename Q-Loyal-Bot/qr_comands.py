import io
import segno

def generate_qr(qr_token: str, bot_username: str):
    # Формируем ссылку для глубокого входа (Deep Link)
    bot_url = f"https://t.me/{bot_username}?start=qr_{qr_token}"
    
    qr = segno.make(bot_url, error='h')
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=2)
    out.seek(0)
    return out