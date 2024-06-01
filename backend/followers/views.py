from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Follower
from .serializers import FollowerSerializer, UserSerializer

class FollowListCreate(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        followee_id = self.request.data.get('followee_id')
        if followee_id:
            try:
                followee = User.objects.get(id=followee_id)
                if Follower.objects.filter(follower=self.request.user, followee=followee).exists():
                    raise ValidationError("You are already following this user.")
                serializer.save(follower=self.request.user, followee=followee)
            except User.DoesNotExist:
                raise ValidationError("User does not exist.")

class Unfollow(generics.DestroyAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        followee_id = self.request.data.get('followee_id')
        try:
            followee = User.objects.get(id=followee_id)
            return Follower.objects.get(follower=self.request.user, followee=followee)
        except User.DoesNotExist:
            raise ValidationError("User does not exist.")
        except Follower.DoesNotExist:
            raise ValidationError("You are not following this user.")

class UserFollowers(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(followers__follower_id=user_id)

class UserFollowing(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(following__followee_id=user_id)
