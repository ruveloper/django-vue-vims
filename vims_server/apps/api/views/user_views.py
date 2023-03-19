from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import (
    UserDetailSerializer,
    UserFavoriteImageSerializer,
    UserImageSerializer,
)
from apps.core.models import UserFavoriteImage, UserImage

User = get_user_model()


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, format=None):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


class UserImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserImageSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return UserImage.objects.filter(user_data__user=self.request.user)


class UserFavoriteImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFavoriteImageSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return UserFavoriteImage.objects.filter(user_data__user=self.request.user)
