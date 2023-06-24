from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    user_type = models.CharField(
        max_length=5, choices=USER_TYPE_CHOICES, default="user"
    )
