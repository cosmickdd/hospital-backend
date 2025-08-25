import os
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .email_verification import EmailVerificationToken
from django.utils import timezone
from datetime import timedelta
from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

# Password Reset Views
from django.contrib.auth import get_user_model
User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if user exists
            return Response({'detail': 'If this email is registered, a password reset link has been sent.'}, status=200)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/reset-password/{uid}/{token}/"
        subject = 'Reset your Sahib Ayurveda password'
        message = f"Click the link to reset your password: {reset_link}"
        email_msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_msg.send(fail_silently=True)
        return Response({'detail': 'If this email is registered, a password reset link has been sent.'}, status=200)

class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required.'}, status=400)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link.'}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=400)
        user.set_password(password)
        user.save()
        # Send password reset confirmation email
        subject = 'Your Sahib Ayurveda password was reset'
        message = f"Hello {user.username},\n\nYour password was successfully reset. If you did not perform this action, please contact support immediately."
        email_msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_msg.send(fail_silently=True)
        return Response({'detail': 'Password has been reset.'}, status=200)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
class ActivateAccountView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(settings.FRONTEND_URL + '/login?verified=1')
        else:
            return Response({'error': 'Activation link is invalid!'}, status=400)
# accounts/views.py

from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileUpdateSerializer, PasswordChangeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        # Generate a secure UUID token, valid for 24 hours
        try:
            token_obj = EmailVerificationToken.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=24)
            )
        except Exception as e:
            user.delete()
            raise e
        backend_domain = getattr(settings, 'BACKEND_DOMAIN', None) or os.environ.get('BACKEND_DOMAIN')
        if not backend_domain:
            backend_domain = 'https://your-backend.onrender.com'
        # Support for 'next' param in registration
    next_url = self.request.data.get('next') if hasattr(self.request, 'data') else None
        verify_link = f"{backend_domain}/api/accounts/verify/?token={token_obj.token}"
        if next_url:
            from urllib.parse import urlencode
            verify_link += '&' + urlencode({'next': next_url})
        mail_subject = 'Activate your Sahib Ayurveda Account'
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'activation_link': verify_link,
            'year': 2025,
        })
        from django.core.mail import EmailMultiAlternatives
        email = EmailMultiAlternatives(
            mail_subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)

# Email verification endpoint
class VerifyEmailTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required.'}, status=400)
        try:
            token_obj = EmailVerificationToken.objects.get(token=token, used=False)
        except EmailVerificationToken.DoesNotExist:
            return Response({'error': 'Invalid or expired token.'}, status=400)
        if token_obj.is_expired():
            return Response({'error': 'Token expired.'}, status=400)
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.used = True
        token_obj.save()
        return Response({'detail': 'Account activated.'}, status=200)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'password set'}, status=status.HTTP_200_OK)

class LogoutView(TokenBlacklistView):
    permission_classes = (IsAuthenticated,)

# Custom role-based permission
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class SessionCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'detail': 'Session is valid.'}, status=200)
