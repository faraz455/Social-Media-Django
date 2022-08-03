from rest_framework import generics
from .serializers import CustomUser, Posts, Follower, CustomUserSerializer, PostsSerializer, FollowerSerializer

class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PostsLCView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class PostsRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class FollowerLCView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

class FollowerRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
