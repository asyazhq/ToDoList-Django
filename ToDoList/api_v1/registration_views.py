from .authentication import UsernameBackendModel
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import request_utils
from . import models

def retrieve_username_and_password(request):
    """
        Extract the username and password from a request

        :param request: The request
    """
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    return username, password


class UserAuthenticationView(APIView):
    """
        Post and generate the authentication as well as login
    """
    def post(self, request, format=None):
        """
            Post method used to authenticate the user
            :param request: The request on a django request format
            :param format: The request format
        """
        username, password = retrieve_username_and_password(request)
        authentication_backend = UsernameBackendModel() 
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'errors': 'The requested user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        cache.set(request.session.session_key, user.username, 60*60*24)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    """
        Post to register a user
    """
    def post(self, request, format=None):
        """
            Post request to register a user
            :param request: The request being sent
            :param format: The format of the request
        """
        if request_utils.is_user_authenticated(request):
            return Response({'errors': 'User is already authenticated'}, status=status.HTTP_400_BAD_REQUEST)

        username, password = retrieve_username_and_password(request)
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()

        if not username or not password:
            return Response({'errors': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'errors': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        user = models.UserModel.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        if not user:
            return Response({'errors': 'The username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
        Logout the user
    """
    def get(self, request, format=None):
        """
            Logout from the API

            :param request: The request
            :param format: The format of the request
        """
        if not request_utils.is_user_authenticated(request):
            return Response({'errors': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache.delete(request.session.session_key)
        logout(request)
        return Response(status=status.HTTP_200_OK)
