# core/views.py
from rest_framework import generics, permissions
from .models import NewsletterSubscription
from .serializers import NewsletterSubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from appointments.models import Appointment
from blog.models import TherapyArticle
from prana_ai.models import DiagnosisMedia
from contact.models import ContactMessage
from django.utils import timezone
from datetime import timedelta

class NewsletterSubscriptionCreateView(generics.CreateAPIView):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = (permissions.AllowAny,)

class AdminDashboardStatsView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        total_users = User.objects.count()
        total_appointments_week = Appointment.objects.filter(created_at__gte=week_ago).count()
        total_appointments_month = Appointment.objects.filter(created_at__gte=month_ago).count()
        top_blog_posts = TherapyArticle.objects.order_by('-id')[:5].values('title', 'slug')
        recent_diagnosis = DiagnosisMedia.objects.order_by('-uploaded_at')[:5].values('user__username', 'status', 'uploaded_at')
        contact_messages = ContactMessage.objects.order_by('-created_at')[:5].values('name', 'email', 'created_at')
        return Response({
            'total_users': total_users,
            'total_appointments_week': total_appointments_week,
            'total_appointments_month': total_appointments_month,
            'top_blog_posts': list(top_blog_posts),
            'recent_diagnosis': list(recent_diagnosis),
            'contact_messages': list(contact_messages),
        })
