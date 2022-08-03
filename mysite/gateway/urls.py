from django.urls import path
from .views import LoginView, RegisterView, feed, timeline


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('feed/', feed.as_view()),
    path('timeline/', timeline.as_view())
]