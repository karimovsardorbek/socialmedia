from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'type', 'related_id', 'timestamp', 'read']
        read_only_fields = ['user', 'timestamp']
