from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, views, permissions
from users.api import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import ProfileSerializer

User = get_user_model()


class RegistrationAPIView(views.APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid():
            serializer.save()
            user = serializer.data

            return Response({
                "data": user,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginApiView(views.APIView):

    def post(self, request):

        data = request.data
        username = data.get('username_or_email')
        password = data.get('password')
        user = authenticate(email=username, password=password)

        if username is None or password is None:
            return None

            user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "invalide username or password"}, status=204)
        try:

            user_token = get_tokens_for_user(user)

            response = {
                "access_token": str(user_token.get("access")),
                "refresh_token": str(user_token.get("refresh"))
            }
            return Response(response)
        except Exception as e:
            raise e


class ProfileViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = ProfileSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
