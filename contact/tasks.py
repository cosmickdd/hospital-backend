# contact/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

def get_contact_email_content(name, email, message):
    return f"New contact form submission from {name} <{email}>:\n\n{message}"

@shared_task(bind=True)
def send_contact_email(self, name, email, message):
    subject = 'New Contact Form Submission'
    content = get_contact_email_content(name, email, message)
    send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
    return 'Contact email sent.'
