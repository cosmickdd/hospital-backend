# appointments/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Appointment
from django.conf import settings

def get_appointment_email_content(appointment):
    return f"Appointment confirmed for {appointment.therapy.name} with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date} at {appointment.time}."

def get_reminder_email_content(appointment):
    return f"Reminder: You have an appointment for {appointment.therapy.name} with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date} at {appointment.time}."

def get_cancellation_email_content(appointment):
    return f"Your appointment for {appointment.therapy.name} with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date} at {appointment.time} has been cancelled."

@shared_task(bind=True)
def send_appointment_confirmation(self, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        subject = 'Appointment Confirmation'
        message = get_appointment_email_content(appointment)
        recipient_list = [appointment.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        appointment.confirmed = True
        appointment.save()
        return 'Email sent and appointment confirmed.'
    except Exception as e:
        return str(e)


# Send reminder email (to be scheduled by Celery beat or manually)
@shared_task(bind=True)
def send_appointment_reminder(self, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        subject = 'Appointment Reminder'
        message = get_reminder_email_content(appointment)
        recipient_list = [appointment.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return 'Reminder email sent.'
    except Exception as e:
        return str(e)

# Send cancellation email
@shared_task(bind=True)
def send_appointment_cancellation(self, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        subject = 'Appointment Cancelled'
        message = get_cancellation_email_content(appointment)
        recipient_list = [appointment.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return 'Cancellation email sent.'
    except Exception as e:
        return str(e)
