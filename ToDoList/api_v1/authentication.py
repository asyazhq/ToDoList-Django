from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsernameBackendModel(ModelBackend):
    """
    Custom authentication backend that allows login using only username and password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate the user using username and password.

        :param request: The HTTP request object
        :param username: The username of the user
        :param password: The password of the user
        :param kwargs: Additional parameters
        """
        UserModel = get_user_model()
        
        if username is None or password is None:
            return None  # Ensure both fields are provided
        
        try:
            # Retrieve the user by username
            user = UserModel.objects.get(username=username)
            
            if user.check_password(password):  # Verify password
                return user
        
        except UserModel.DoesNotExist:
            return None  # Return None if user doesn't exist
        
        return None
