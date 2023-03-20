from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Service


class ListServices(APIView):
    def get(self, request: Request, format=None):
        # * Get available services
        service_models: QuerySet = Service.objects.all()
        available_services: list[str] = [service.service for service in service_models]
        return Response(
            {
                "count": len(available_services),
                "services": available_services,
            }
        )


class ReCaptcha(APIView):
    def get(self, request: Request, format=None):
        # * Send reCaptcha Public Key
        if settings.DEBUG:
            return Response({"key": "MyPublicReCaptchaKey"})
        return Response({"key": settings.RECAPTCHA_PUBLIC_KEY})
