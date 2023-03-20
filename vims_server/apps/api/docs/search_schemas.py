from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes

get_search_schema = [
    OpenApiParameter(
        name="query",
        description="A query string",
        type=OpenApiTypes.STR,
        required=True,
    ),
    OpenApiParameter(
        name="page",
        description="The page number",
        type=OpenApiTypes.INT,
        required=False,
    ),
    OpenApiParameter(
        name="per_page",
        description="The number of results per page",
        type=OpenApiTypes.INT,
        required=False,
    ),
    OpenApiParameter(
        name="service",
        description="A list of services to search in, obtainable from /api/services",
        type={"type": "array", "items": {"type": "string"}},
        required=True,
    ),
]
