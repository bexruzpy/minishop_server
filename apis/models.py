from django.db import models
from .utils import create_license
from django.utils import timezone
from django.conf import settings

# This class represents a user model in a Python application.
class User(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13, unique=True)
    about_shop = models.TextField(default="")
    device_id = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DeviceToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.JSONField(default=dict())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token["data"]
    def save(self, *args, **kwargs):
        
        if not self.token:  # agar token hali yaratilmagan bo‘lsa
            self.token = self.generate_token()
        super().save(*args, **kwargs)
        
    def generate_token(self):
        return create_license(
            {
                "device_id": self.user.device_id,
                "product": settings.PROJECT_NAME
            }
        )