from dataclasses import asdict

from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.docs.search_schemas import get_search_schema
from apps.api.serializers import SearchParamsSerializer
from apps.core.models import Service
from apps.services import PexelsApi, PixabayApi, UnsplashApi


class Search(APIView):
    throttle_scope = "search"

    @extend_schema(parameters=get_search_schema)
    def get(self, request: Request, format=None):
        # * Validate query params
        serializer = SearchParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # * Get validated query parameters
        services = validated_data.get("service", [])
        query = validated_data.get("query", None)
        page = validated_data.get("page", 1)
        per_page = validated_data.get("per_page", 10)

        # * Get available services
        service_models: QuerySet = Service.objects.all()
        available_services: list[str] = [service.service for service in service_models]

        # * Performs api requests
        results: list[dict] = []
        for service in services:
            service_model: Service = service_models.get(service=service)

            images: list[dict] = []
            if service in available_services and service == "pexels":
                images = [
                    asdict(api_image)
                    for api_image in PexelsApi(service_model).search(
                        query, page, per_page
                    )
                ]
            elif service in available_services and service == "unsplash":
                images = [
                    asdict(api_image)
                    for api_image in UnsplashApi(service_model).search(
                        query, page, per_page
                    )
                ]
            elif service in available_services and service == "pixabay":
                images = [
                    asdict(api_image)
                    for api_image in PixabayApi(service_model).search(
                        query, page, per_page
                    )
                ]
            else:
                continue

            results.append(
                {
                    "service": service,
                    "images": images,
                }
            )

        # * Format response
        response_data: dict = {
            "page": page,
            "per_page": per_page,
            "results": results,
        }

        return Response(response_data)
