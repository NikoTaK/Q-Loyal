from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
import os

def decode_qr(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)

    if not decoded_objects:
        return None

    return decoded_objects[0].data.decode("utf-8")

def generate_qr(user_id):
    os.makedirs("qrs", exist_ok=True)
    qr_data = f"tg_user:{user_id}"
    file_path = f"qrs/{user_id}.png"

    img = qrcode.make(qr_data)
    img.save(file_path)

    return file_path