from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver_id')
        content = self.request.data.get('content')
        if receiver_id and content:
            try:
                receiver = User.objects.get(id=receiver_id)
                serializer.save(sender=self.request.user, receiver=receiver, content=content)
            except User.DoesNotExist:
                raise ValidationError("Receiver does not exist.")
        else:
            raise ValidationError("Receiver ID and content are required.")

class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        message = super().get_object()
        if self.request.user != message.sender and self.request.user != message.receiver:
            raise ValidationError("You do not have permission to view this message.")
        return message
