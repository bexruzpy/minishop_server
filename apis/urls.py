from django.urls import path
from .views import ariza_yuborish

urlpatterns = [
    path("send_request/", ariza_yuborish, name="send_request"),
]