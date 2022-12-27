from django.contrib.auth import get_user_model
# rest framework
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# simple jwt
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# serializers
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    GoogleLoginSerializer,
)
# helpers
from utils.helpers import get_random_name, get_auth_token


User = get_user_model()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_auth_token(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh_token": token['refresh'],
            "access_token": token['access'],
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = get_auth_token(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh_token": token['refresh'],
            "access_token": token['access'],
        })


class UserAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def post(self, _):
        user = self.request.user
        user.is_onboarded = True
        user.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class RefreshTokenAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data

        return Response({
            "refresh_token": token['refresh'],
            "access_token": token['access'],
        })


class GoogleOAuthAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = get_auth_token(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh_token": token['refresh'],
            "access_token": token['access'],
        })


class RandomNameAPI(APIView):

    def get(self, _):
        random_name = get_random_name()

        # FIXME: find a better way to do it, since it might make a lot of queries to the database
        while User.objects.filter(username=random_name).exists():
            random_name = get_random_name()

        return Response({
            "name": random_name
        })
