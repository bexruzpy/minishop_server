from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bot.bot_init import bot
from bot.utils import create_post
from rest_framework import serializers, status
import asyncio, json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from urllib.parse import parse_qs


# Serializer view ichida
class ArizaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=13)
    device_id = serializers.CharField(max_length=500)
    about_shop = serializers.CharField(max_length=500)
    def send_message(self):
        return bot.send_message(**create_post(**self.validated_data))
        


@csrf_exempt
async def ariza_yuborish(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    body_str = request.body.decode("utf-8")
    data_dict = {k: v[0] for k, v in parse_qs(body_str).items()}
    serializer = ArizaSerializer(data=data_dict)
    if serializer.is_valid():
        try:
            await serializer.send_message()
            return JsonResponse(
                {
                    "message": "Ariza qabul qilindi!\nTez orada bepul sinab ko'rish ochiladi va o'zimiz sizga aloqaga chiqamiz."
                },
                status=201
            )
        except Exception as e:
            print(str(e))
            return JsonResponse({"detail": "Judayam ko'p urunishlar keyinroq urunib ko'ring"}, status=400)
    return JsonResponse(
        {
            "detail": "Ma'lumotlar xato"
        },
        status=400
    )


