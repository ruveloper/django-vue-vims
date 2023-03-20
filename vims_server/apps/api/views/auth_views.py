from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.helpers import validate_recaptcha_form
from apps.api.serializers import RegisterSerializer
from apps.core.models import User as User_Model

User: User_Model = get_user_model()


class TokenLogin(ObtainAuthToken):
    def post(self, request: Request, *args, **kwargs):
        # * reCaptcha Form Validation
        validate_recaptcha_form(request)
        return super().post(request, *args, **kwargs)


class TokenLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, format=None):
        try:
            request.user.auth_token.delete()
            return Response(
                {"success": "User logged out successfully"}, status=status.HTTP_200_OK
            )
        except:  # noqa
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class Registration(APIView):
    def post(self, request: Request, format=None):
        # * reCaptcha Form Validation
        validate_recaptcha_form(request)
        # * Fields Validation
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                email=serializer.validated_data["email"],
                name=serializer.validated_data["name"],
            )
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
