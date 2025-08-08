# prana_ai/serializers.py
from rest_framework import serializers
from .models import DiagnosisMedia

class DiagnosisMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisMedia
        fields = '__all__'
        read_only_fields = ('user', 'status', 'report', 'uploaded_at')
