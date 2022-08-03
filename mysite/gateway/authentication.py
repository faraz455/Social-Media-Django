import jwt
from django.conf import settings
from datetime import datetime
from rest_framework.authentication import BaseAuthentication
from user.models import CustomUser

class Authentication(BaseAuthentication):

    def authenticate(self,request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None
        return self.get_user(data['user_id']), None

    # get user by user.id
    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id = user_id)
            return user
        except Exception:
            return None

    # validate the request if the request is by the login user
    def validate_request(self, headers):
        authorization = headers.get('Authorization', None)
        if not authorization:
            return None
        # remove bearer word from token to get exact token value
        token = headers['Authorization'][7:]
        # varify the token
        decoded_data = self.varify_token(token)
        # incase of token invalid
        if not decoded_data:
            return None
        return decoded_data

    # Function used by class below to varify the token
    @staticmethod
    def varify_token(token):
        # decode the token
        try:
            decoded_data = jwt.decode(token,settings.SECRET_KEY, algorithms="HS256")
        except Exception:
            return None
        # check if token expires
        exp = decoded_data['exp']
        if datetime.now().timestamp() > exp:
            return None
        return decoded_data

