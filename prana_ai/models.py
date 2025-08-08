# prana_ai/models.py
from django.db import models
from accounts.models import User

class DiagnosisMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='diagnosis_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    report = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
