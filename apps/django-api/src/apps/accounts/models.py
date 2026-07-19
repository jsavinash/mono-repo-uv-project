from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with additional fields."""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    bio = models.TextField(max_length=500, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(blank=True, null=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    theme = models.CharField(
        max_length=20, choices=[("light", "Light"), ("dark", "Dark")], default="light"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email or self.username
