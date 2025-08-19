import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import Dispatcher
from aiogram.types import Update
from .bot_init import dp, bot   # siz yaratgan dp
from django.conf import settings


@csrf_exempt
async def telegram_webhook(request, token):
    print(request.method, token == settings.BOT_TOKEN)

    if token != settings.BOT_TOKEN:
        return JsonResponse({"ok": False, "error": "Invalid token"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))   # Telegram yuborgan JSON
            telegram_update = Update.model_validate(data)     # Aiogram Update obyektiga aylantirish
            await dp.feed_update(bot=bot, update=telegram_update)  # dispatcher ga yuborish
        except Exception as e:
            print("Webhook error:", e)
            return JsonResponse({"ok": False, "error": str(e)}, status=500)

        return JsonResponse({"ok": True}, status=200)

    return JsonResponse({"ok": False, "error": "Invalid method"}, status=405)


