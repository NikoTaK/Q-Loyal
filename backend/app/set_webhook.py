import requests
from app.config import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
WEBHOOK_URL = "https://osiered-amal-glancingly.ngrok-free.dev/telegram/webhook"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
)
print(response.json())
