from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Notification
from .serializers import NotificationSerializer

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        notification = super().get_object()
        if self.request.user != notification.user:
            raise PermissionDenied("You do not have permission to view this notification.")
        return notification

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.read:
            self.send_notification(instance)

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_notification(instance)

    def send_notification(self, notification):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{notification.user.id}",
            {
                "type": "send_notification",
                "notification": NotificationSerializer(notification).data,
            },
        )
