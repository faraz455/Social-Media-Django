from rest_framework import serializers
from .models import CustomUser, Posts, Follower

class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):

    posts = PostsSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'

