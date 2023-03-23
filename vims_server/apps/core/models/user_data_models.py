from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.utils import media_user_path
from apps.core.validators import MaxFileSizeValidator

User = get_user_model()


class UserData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # * Data Fields
    max_user_images = models.IntegerField(default=20, editable=False)
    max_user_favorites = models.IntegerField(default=200, editable=False)

    # * Relations
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_max_user_images_field(self, new_value: int):
        self.max_user_images = new_value
        self.save()

    def update_max_user_favorites_field(self, new_value: int):
        self.max_user_favorites = new_value
        self.save()

    def __str__(self):
        return f"{str(self.user)} data"

    class Meta:
        verbose_name = "User Data"
        verbose_name_plural = "User Data"


class UserImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255, default="No Name")
    image = models.ImageField(
        upload_to=media_user_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
            MaxFileSizeValidator(kilobytes=1000),
        ],
    )

    # * Relations
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def clean(self):
        # * Non Fields Validations
        # Validate the max number of images allowed for the current user.
        max_number = self.user_data.max_user_images
        current_number = UserImage.objects.filter(user_data=self.user_data).count()
        if current_number > max_number:
            raise ValidationError(
                "Max number of images for the current user has been exceeded."
            )
        return super().clean()

    def __str__(self):
        return f"Image {self.name}"

    class Meta:
        ordering = ["-created"]


class UserFavoriteImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    service = models.CharField(max_length=255, default="No Service")
    image_id = models.CharField(max_length=255, default="No Image ID")
    author = models.CharField(max_length=255, default="No Author")
    name = models.CharField(max_length=255, default="No Name")
    link = models.URLField()
    preview_url = models.URLField()
    original_url = models.URLField()

    # * Relations
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def clean(self):
        # * Non Fields Validations
        # Validate the max number of favorites allowed for the current user.
        max_number = self.user_data.max_user_favorites
        current_number = UserFavoriteImage.objects.filter(
            user_data=self.user_data
        ).count()
        if current_number > max_number:
            raise ValidationError(
                "Max number of favorite images for the current user has been exceeded."
            )
        return super().clean()

    def __str__(self):
        return f"Favorite {self.name}"

    class Meta:
        verbose_name = "Favorite Image"
        verbose_name_plural = "Favorite Images"
        ordering = ["-created"]
