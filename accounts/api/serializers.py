from django.contrib.auth import authenticate, get_user_model
# rest framework
from rest_framework import serializers
# local
from utils.helpers import validate_google_token, get_random_name

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_onboarded',)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField()
    client_id = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        client_id = data.get('client_id')
        email = validate_google_token(token, client_id)["email"]

        if not email:
            raise serializers.ValidationError("Invalid Token")

        user = User.objects.filter(email=email).first()

        if user:
            return user
        else:
            username = get_random_name()

            # FIXME: find a better way to do it, since it might make a lot of queries to the database
            while User.objects.filter(username=username).exists():
                username = get_random_name()

            user = User.objects.create_user(
                email=email,
                password=None,
                username=username,
            )
            return user
