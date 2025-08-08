# prana_ai/urls.py
from django.urls import path
from .views import DiagnosisMediaUploadView, DiagnosisMediaListView, DiagnosisMediaDetailView

urlpatterns = [
    path('upload/', DiagnosisMediaUploadView.as_view(), name='diagnosis_upload'),
    path('my/', DiagnosisMediaListView.as_view(), name='diagnosis_list'),
    path('report/<int:pk>/', DiagnosisMediaDetailView.as_view(), name='diagnosis_detail'),
]
