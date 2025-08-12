# core/serializers.py
from rest_framework import serializers
from .models import NewsletterSubscription
class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = '__all__'
        read_only_fields = ('subscribed_at',)
