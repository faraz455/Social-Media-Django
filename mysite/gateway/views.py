import jwt
from .models import Jwt
from user.models import CustomUser, Follower, Posts
from user.serializers import FollowerSerializer, PostsSerializer
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from .serializer import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
# Get random data for refresh token
def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase +string.digits,k =length))

# Token that need to be provide by user to server
def get_access_token(payload):
    return jwt.encode(
        # expiration is set 5 minutes so that user cant access server for long time
        {"exp": datetime.now()+ timedelta(minutes = 5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

# Token that is issued by server to the user 
def get_refresh_token():
    return jwt.encode(
        # expiration time set to an year so it remain login till user logouts
        {"exp": datetime.now()+timedelta(days=365),"data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

# Login view created to login the registered user
class LoginView(ListAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        # valids the data
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception = True)

        # check if the user name and password matches the existing user data
        user = authenticate(
            username = serializer.validated_data['email'], 
            password = serializer.validated_data['password']
            )
        # incase user doesnt exist
        if not user:
            return Response({"Error": " Invalid Email or password"}, status="400")
        Jwt.objects.filter(user_id = user.id).delete()
        # access and refresh token created
        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()
        # Jwt class object created
        Jwt.objects.create(
            user_id = user.id , access = access.decode(), refresh = refresh.decode()
        )
        return Response({"access": access, "refresh" : refresh})

# Register view created to register the new user 
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception = True)
          
        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"success": "user created."})

class feed(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        id = int(request.GET.get('id'))
        serializer = FollowerSerializer(Follower.objects.filter(follower_obj=id), many=True)

        following_users = []
        for user in serializer.data:
            following_users.append(user['user_obj'])

        serializer = PostsSerializer(Posts.objects.filter(post_user__in = following_users), many=True)
        return Response(serializer.data)

class timeline(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        id = int(request.GET.get('id'))
        serializer = PostsSerializer(Posts.objects.filter(post_user = id), many=True)
        return Response(serializer.data)
