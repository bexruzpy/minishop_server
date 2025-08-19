from django.conf import settings

from aiogram import Router, types, F
from asgiref.sync import sync_to_async

from aiogram.filters import Command
from rest_framework.response import Response
from rest_framework import serializers
from apis.models import User, DeviceToken
from .utils import create_post, parse_formatted_message
from .bot_init import bot
from io import BytesIO

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ["created_at", "updated_at"]

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = "__all__"
        read_only_fields = ["token", "created_at", "updated_at"]




router = Router()

@router.message(F.chat.id != settings.ADMIN_TELEGRAM_ID)
async def none(message: types.Message):
    pass

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum hush kelibsiz!")

@router.callback_query(F.data == "activate_one_month")
async def echo(call: types.CallbackQuery):
    data = parse_formatted_message(call.message.text)
    print(data)
@router.callback_query(F.data == "download_key_file")
async def echo(call: types.CallbackQuery):
    data = parse_formatted_message(call.message.text)  # e.g. {'name': 'Bexruz', 'phone': '+998...'}

    # 1) User serializer
    user_ser = UserSerializer(data=data)
    user = User.objects.get(device_id=data["device_id"], phone=data["phone"])
    print(UserSerializer(user).data)

    # 2) Save user
    try:
        user = await sync_to_async(user_ser.save)()
    except Exception as e:
        await call.message.answer(f"User save error: {str(e)}")
        print("User save exception:", e)
        return

    # 3) DeviceToken serializer
    token_ser = DeviceTokenSerializer(data={"user": user.id})
    if not await sync_to_async(token_ser.is_valid)():
        errors = await sync_to_async(lambda: dict(token_ser.errors))()
        await call.message.answer(f"Ma'lumotlar xato (token):\n{errors}")
        print("Token serializer errors:", errors)
        return

    try:
        token = await sync_to_async(token_ser.save)()
    except Exception as e:
        await call.message.answer(f"Token save error: {str(e)}")
        print("Token save exception:", e)
        return

    # 4) yuborish
    file = BytesIO(json.dumps({"token": str(token.token)}, indent=4).encode("utf-8"))
    file.name = f"{user.name}.key"
    await bot.send_document(chat_id=call.message.chat.id, document=file)


@router.callback_query(F.data == "close")
async def echo(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

