# accounts/urls.py

from django.urls import path
from .views import RegisterView, UserDetailView, ProfileUpdateView, PasswordChangeView, LogoutView, SessionCheckView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('me/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('me/change-password/', PasswordChangeView.as_view(), name='password_change'),
    path('session/', SessionCheckView.as_view(), name='session_check'),
]
