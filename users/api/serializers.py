from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            password=validated_data.get("password")
        )
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    access_token = serializers.CharField(max_length=256, read_only=True)
    refresh_token = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "access_token", "refresh_token")

    def validate(self, data):
        username = data.get("username")
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("invalid username or password")

        try:
            user_token = get_tokens_for_user(user)
            return {
                "access_token": str(user_token.get("access")),
                "refresh_token": str(user_token.get("refresh"))
            }
        except Exception as e:
            raise e


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username",]
