# accounts/serializers.py

from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_doctor', 'is_admin', 'phone')
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')
        extra_kwargs = {'username': {'required': False}, 'email': {'required': False}, 'phone': {'required': False}}

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_doctor')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_doctor=validated_data.get('is_doctor', False)
        )
        return user
