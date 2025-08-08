from django.test import TestCase
from django.contrib.auth import get_user_model
from prana_ai.models import DiagnosisMedia
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class DiagnosisMediaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_diagnosis_media(self):
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        media = DiagnosisMedia.objects.create(user=self.user, file=file)
        self.assertEqual(media.status, 'pending')
        self.assertIsNone(media.report)
        self.assertEqual(str(media), f"{self.user.username} - pending")

    def test_status_and_report(self):
        file = SimpleUploadedFile("test2.jpg", b"file_content", content_type="image/jpeg")
        media = DiagnosisMedia.objects.create(user=self.user, file=file)
        media.status = 'completed'
        media.report = "Diagnosis: Healthy"
        media.save()
        self.assertEqual(media.status, 'completed')
        self.assertEqual(media.report, "Diagnosis: Healthy")