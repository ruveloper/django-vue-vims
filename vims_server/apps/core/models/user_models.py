from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.utils import media_user_path
from apps.core.validators import MaxFileSizeValidator


class User(AbstractUser):
    """
    Default custom user model for vims.
    """

    #: First and last name do not cover global name patterns
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField(blank=True, max_length=255)

    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to=media_user_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            MaxFileSizeValidator(kilobytes=1000),
        ],
    )
