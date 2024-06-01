from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Follower

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followee = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followee', 'timestamp']
