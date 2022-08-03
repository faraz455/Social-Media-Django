from django.urls import path
from .views import CustomUserListView, CustomUserRUDView, PostsLCView ,PostsRUDView, FollowerLCView

urlpatterns = [
    path('user/', CustomUserListView.as_view()),
    path('user/<int:pk>/', CustomUserRUDView.as_view()),
    path('posts/', PostsLCView.as_view()),
    path('posts/<int:pk>/', PostsRUDView.as_view()),
    path('follower/', FollowerLCView.as_view()),    
]
