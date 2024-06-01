from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Comment
from .serializers import CommentSerializer

class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise PermissionDenied('You do not have permission to edit this comment.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied('You do not have permission to delete this comment.')
        instance.delete()
