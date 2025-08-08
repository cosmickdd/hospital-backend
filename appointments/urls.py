# appointments/urls.py
from django.urls import path
from .views import (
    TherapyListView, TherapyDetailView, AppointmentCreateView, AppointmentListView,
    AppointmentCancelView, AppointmentRescheduleView, DoctorListView,
    UpcomingAppointmentsView, PastAppointmentsView,
    AllAppointmentsView, DoctorAppointmentsView
)

urlpatterns = [
    path('therapies/', TherapyListView.as_view(), name='therapy_list'),
    path('therapies/<int:pk>/', TherapyDetailView.as_view(), name='therapy_detail'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('my-appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('my-appointments/upcoming/', UpcomingAppointmentsView.as_view(), name='upcoming_appointments'),
    path('my-appointments/past/', PastAppointmentsView.as_view(), name='past_appointments'),
    path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('appointments/<int:pk>/reschedule/', AppointmentRescheduleView.as_view(), name='appointment_reschedule'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('admin/all-appointments/', AllAppointmentsView.as_view(), name='all_appointments'),
    path('doctor/my-appointments/', DoctorAppointmentsView.as_view(), name='doctor_appointments'),
]
