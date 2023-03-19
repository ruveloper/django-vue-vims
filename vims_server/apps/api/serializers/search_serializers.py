from rest_framework import serializers


class SearchParamsSerializer(serializers.Serializer):
    service = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,  # Ensure at least one service is provided
        required=True,
    )
    query = serializers.CharField(max_length=100, required=True)
    page = serializers.IntegerField(min_value=1, max_value=50, required=False)
    per_page = serializers.IntegerField(min_value=5, max_value=100, required=False)
