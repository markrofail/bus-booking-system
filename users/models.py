from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    payment_info = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
