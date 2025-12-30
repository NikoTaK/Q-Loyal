import io
import segno

def generate_qr(qr_token: str):

    bot_url = f"https://t.me/QLoyal_bot?start=qr_{qr_token}"
    
    qr = segno.make(bot_url, error='h')

    out = io.BytesIO()
    qr.save(out, kind='png', scale=10)
    out.seek(0)

    return out