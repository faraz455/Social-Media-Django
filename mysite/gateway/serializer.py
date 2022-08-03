from rest_framework import serializers
from .models import Jwt
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField() 

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField() 
    name = serializers.CharField() 

class JwtSerializer(serializers.Serializer):

    class Meta:
        model = Jwt
        fields = '__all__'