# blog/serializers.py
from rest_framework import serializers
from .models import TherapyArticle

class TherapyArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapyArticle
        fields = '__all__'
