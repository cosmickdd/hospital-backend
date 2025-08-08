# appointments/models.py
from django.db import models
from accounts.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Therapy(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField()
    benefits = models.TextField()
    duration = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.therapy.name} on {self.date}"
