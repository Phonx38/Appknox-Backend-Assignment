from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import (
    UserCreateSerializer,
    AdminCreateSerializer,
    UserLoginSerializer,
)
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiExample


User = get_user_model()


@extend_schema(
    description="Create a new normal user.",
    examples=[
        OpenApiExample(
            "User Creation Example",
            value={
                "username": "newuser",
                "password": "mypassword",
            },
        ),
    ],
)
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@extend_schema(
    description="Create a new admin user.",
    examples=[
        OpenApiExample(
            "Admin Creation Example",
            value={
                "username": "newadmin",
                "password": "adminpassword",
            },
        ),
    ],
)
class AdminCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCreateSerializer


@extend_schema(
    description="Login for both admin and normal users.",
    examples=[
        OpenApiExample(
            "User Login Example",
            value={
                "username": "existinguser",
                "password": "existingpassword",
            },
        ),
    ],
)
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
