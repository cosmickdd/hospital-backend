import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at or self.used

    def __str__(self):
        return f"{self.user.email} - {self.token}"
