# prana_ai/views.py
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import DiagnosisMedia
from .serializers import DiagnosisMediaSerializer
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from django.conf import settings
import mimetypes

ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'video/mp4']

from django_ratelimit.decorators import ratelimit

class DiagnosisMediaUploadView(generics.CreateAPIView):
    queryset = DiagnosisMedia.objects.all()
    serializer_class = DiagnosisMediaSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)

    @ratelimit(key='user', rate='5/m', block=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        if file:
            mime_type, _ = mimetypes.guess_type(file.name)
            if mime_type not in ALLOWED_MIME_TYPES:
                raise ValidationError('Only JPG, PNG, and MP4 files are allowed.')
        instance = serializer.save(user=self.request.user)
        from .tasks import process_diagnosis_media
        process_diagnosis_media.delay(instance.id)

class DiagnosisMediaListView(generics.ListAPIView):
    serializer_class = DiagnosisMediaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DiagnosisMedia.objects.filter(user=self.request.user)


# API to fetch a single report and status
class DiagnosisMediaDetailView(generics.RetrieveAPIView):
    queryset = DiagnosisMedia.objects.all()
    serializer_class = DiagnosisMediaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DiagnosisMedia.objects.filter(user=self.request.user)
