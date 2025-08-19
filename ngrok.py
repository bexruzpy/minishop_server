import requests
from pyngrok import ngrok

import os

# .env faylni yuklash
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.environ.get('BOT_TOKEN')

if __name__ == "__main__":
    # Django serverni ngrok orqali ochamiz (lokalda test uchun)
    public_url = ngrok.connect(8000).public_url
    print("Ngrok URL:", public_url)

    # Webhookni sozlash
    webhook_url = f"{public_url}/webhook/{TOKEN}/"
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")
    print("SetWebhook response:", res.json())
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()

