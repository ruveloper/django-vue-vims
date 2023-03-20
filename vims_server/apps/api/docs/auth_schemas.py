from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

post_logout_schema = [
    OpenApiParameter(
        name="Authorization",
        description="Authorization token",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.HEADER,
        required=True,
        examples=[
            OpenApiExample(
                "Token Example", value="Token 88f3b3b27278e47ffc2e638c9633d5cfbe528e4d"
            )
        ],
    ),
]
