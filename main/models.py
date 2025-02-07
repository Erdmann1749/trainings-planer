from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [('trainer', 'Trainer'), ('student', 'Student')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True)

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "trainer")  # Trainer-Rolle setzen
        return self.create_user(username, email, password, **extra_fields)
