from django.urls import path
from .views import MessageListCreate, MessageDetail

urlpatterns = [
    path('', MessageListCreate.as_view(), name='message-list-create'),
    path('<int:pk>/', MessageDetail.as_view(), name='message-detail'),
]
