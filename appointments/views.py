
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
    queryset = Therapy.objects.all()
    serializer_class = TherapySerializer
    permission_classes = (permissions.AllowAny,)

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
from rest_framework import status
from rest_framework.response import Response

# Cancel appointment

class AppointmentCancelView(generics.DestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        from appointments.tasks import send_appointment_cancellation
        send_appointment_cancellation.delay(instance.id)
        instance.delete()

# Reschedule appointment
class AppointmentRescheduleView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        date = request.data.get('date', instance.date)
        time = request.data.get('time', instance.time)
        doctor = instance.doctor
        # Check doctor availability and double-booking
        if not doctor or not doctor.available:
            return Response({'doctor': 'Doctor is not available.'}, status=status.HTTP_400_BAD_REQUEST)
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exclude(pk=instance.pk).exists():
            return Response({'non_field_errors': 'This doctor already has an appointment at this time.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.date = date
        instance.time = time
        instance.save()
        return Response(AppointmentSerializer(instance).data)

# List doctors
# List doctors
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# List upcoming appointments for patient
class UpcomingAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        now = timezone.now().date()
        return Appointment.objects.filter(user=self.request.user, date__gte=now).order_by('date', 'time')

# List past appointments for patient
class PastAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        now = timezone.now().date()
        return Appointment.objects.filter(user=self.request.user, date__lt=now).order_by('-date', '-time')

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)
