from . import registration_views
from django.urls import path, re_path, include
from . import urls_name

urlpatterns = [
    re_path(r'^auth/login/',
        registration_views.UserAuthenticationView.as_view(),
        name=urls_name.LOGIN_NAME),
    re_path(r'^auth/logout/',
        registration_views.LogoutView.as_view(),
        name=urls_name.LOGOUT_NAME),
    re_path(r'^auth/register/',
        registration_views.UserRegistrationView.as_view(),
        name=urls_name.REGISTER_NAME),
]