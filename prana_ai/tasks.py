# prana_ai/tasks.py
from celery import shared_task
from .models import DiagnosisMedia
import time

@shared_task(bind=True)
def process_diagnosis_media(self, media_id):
    try:
        media = DiagnosisMedia.objects.get(id=media_id)
        media.status = 'processing'
        media.save()
        # Simulate AI processing
        time.sleep(5)  # Simulate processing time
        # Simulate a diagnosis result
        report = f"AI Diagnosis Report for file {media.file.name}: Healthy."
        media.report = report
        media.status = 'completed'
        media.save()
    except DiagnosisMedia.DoesNotExist:
        return 'Media not found'
    except Exception as e:
        media.status = 'failed'
        media.save()
        return str(e)
    return 'Diagnosis completed'
