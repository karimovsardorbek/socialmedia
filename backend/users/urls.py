from django.urls import path
from .views import UserDetail, ProfileDetail, UserCreate

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-register'),
    path('profile/', ProfileDetail.as_view(), name='user-profile'),
    path('user/', UserDetail.as_view(), name='user-detail'),
]
