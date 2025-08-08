# contact/views.py
from rest_framework import generics, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        instance = serializer.save()
        from .tasks import send_contact_email
        send_contact_email.delay(instance.name, instance.email, instance.message)
