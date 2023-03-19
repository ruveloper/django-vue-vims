from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.models import UserData, UserFavoriteImage, UserImage

User = get_user_model()


class UserFavoriteImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        user_data, created = UserData.objects.get_or_create(user=user)
        user_favorite_image = UserFavoriteImage.objects.create(
            name=validated_data["name"],
            url=validated_data["url"],
            user_data=user_data,
        )
        return user_favorite_image

    class Meta:
        model = UserFavoriteImage
        fields = ("id", "name", "url")


class UserImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        user_data, created = UserData.objects.get_or_create(user=user)
        user_image = UserImage.objects.create(
            name=validated_data["name"],
            image=validated_data["image"],
            user_data=user_data,
        )
        return user_image

    class Meta:
        model = UserImage
        fields = ("id", "name", "image")


class UserDataSerializer(serializers.ModelSerializer):
    userimage_set = UserImageSerializer(many=True)
    userfavoriteimage_set = UserFavoriteImageSerializer(many=True)

    class Meta:
        model = UserData
        fields = (
            "max_user_images",
            "max_user_favorites",
            "userimage_set",
            "userfavoriteimage_set",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    userdata = UserDataSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "name", "email", "userdata"]
