# appointments/serializers.py
from rest_framework import serializers
from .models import Doctor, Therapy, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class TherapySerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapy
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('user', 'confirmed', 'created_at')
