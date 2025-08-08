# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # Add additional fields as needed
