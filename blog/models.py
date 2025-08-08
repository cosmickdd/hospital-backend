# blog/models.py
from django.db import models
from accounts.models import User

class TherapyArticle(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('therapy', 'Therapy'),
        ('news', 'News'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    overview = models.TextField()
    benefits = models.TextField()
    duration = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    doctor = models.ForeignKey('appointments.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='therapy_articles/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
