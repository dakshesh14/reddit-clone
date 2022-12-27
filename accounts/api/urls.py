from django.urls import path

from .api import (
    RegisterAPI,
    LoginAPI,
    UserAPI,
    RandomNameAPI,
    GoogleOAuthAPI
)

urlpatterns = [
    # register
    path('register', RegisterAPI.as_view()),
    # login
    path('login', LoginAPI.as_view()),
    # user details
    path('user', UserAPI.as_view()),
    # randome name suggestion
    path('random-name', RandomNameAPI.as_view(), name='random-name'),
    # google login
    path('google-login', GoogleOAuthAPI.as_view(), name='google-login'),
]
