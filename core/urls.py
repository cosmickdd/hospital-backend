# core/urls.py
from django.urls import path
from .views import NewsletterSubscriptionCreateView, AdminDashboardStatsView
from .views_health import health_check

urlpatterns = [
    path('subscribe/', NewsletterSubscriptionCreateView.as_view(), name='newsletter_subscribe'),
    path('admin-dashboard/', AdminDashboardStatsView.as_view(), name='admin_dashboard_stats'),
    path('health/', health_check, name='health_check'),
]
