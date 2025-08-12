# appointments/views.py

from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from .models import Doctor, Therapy, Appointment
from .serializers import DoctorSerializer, TherapySerializer, AppointmentSerializer

# Admin/doctor: List all appointments (admin only)
class AllAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAdminUser,)
    def get_queryset(self):
        return Appointment.objects.all().order_by('-date', '-time')

# Doctor: List appointments for the logged-in doctor
class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        try:
            doctor = user.doctor
        except Doctor.DoesNotExist:
            return Appointment.objects.none()
        return Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')

class TherapyListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        therapies = [
            {"id": 1, "name": "Abhyanga (Oil Massage)"},
            {"id": 2, "name": "Shirodhara (Oil Pouring on Forehead)"},
            {"id": 3, "name": "Swedana (Herbal Steam Bath)"},
            {"id": 4, "name": "Pizhichil (Oil Squeezing Therapy)"},
            {"id": 5, "name": "Nasya (Nasal Therapy)"},
            {"id": 6, "name": "Basti (Medicated Enema)"},
            {"id": 7, "name": "Udvartana (Herbal Powder Massage)"},
            {"id": 8, "name": "Kati Basti (Lower Back Oil Pooling)"},
            {"id": 9, "name": "Netra Tarpana (Eye Rejuvenation)"},
            {"id": 10, "name": "Vamana (Therapeutic Emesis)"},
        ]
        return Response(therapies)

class TherapyDetailView(generics.RetrieveAPIView):
    queryset = Therapy.objects.all()
    serializer_class = TherapySerializer
    permission_classes = (permissions.AllowAny,)

from django_ratelimit.decorators import ratelimit
class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)
    @ratelimit(key='user', rate='5/m', block=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    def perform_create(self, serializer):
        data = serializer.validated_data
        doctor = data.get('doctor')
        date = data.get('date')
        time = data.get('time')
        # Check doctor availability and double-booking
        if not doctor or not doctor.available:
            raise serializers.ValidationError({'doctor': 'Doctor is not available.'})
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError({'non_field_errors': 'This doctor already has an appointment at this time.'})
        appointment = serializer.save(user=self.request.user)
        from appointments.tasks import send_appointment_confirmation
        send_appointment_confirmation.delay(appointment.id)
