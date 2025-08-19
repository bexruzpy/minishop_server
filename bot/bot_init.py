# bot_init.py
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


API_TOKEN = settings.BOT_TOKEN
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

from .handlers import router
dp.include_router(router)
