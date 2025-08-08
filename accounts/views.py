# accounts/views.py

from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileUpdateSerializer, PasswordChangeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

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
