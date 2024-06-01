from django.urls import path
from .views import FollowListCreate, Unfollow

urlpatterns = [
    path('', FollowListCreate.as_view(), name='follow-list-create'),
    path('unfollow/', Unfollow.as_view(), name='unfollow'),
]
