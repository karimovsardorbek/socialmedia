from django.urls import path
from .views import NotificationList, NotificationDetail

urlpatterns = [
    path('', NotificationList.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetail.as_view(), name='notification-detail'),
]
