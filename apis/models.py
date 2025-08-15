from django.db import models


class User(models.Model):
    name = models.CharField(max_length=150)
    phone = models.EmailField(max_length=100)
    device_id = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)

    def __str__(self):
        return self.token
