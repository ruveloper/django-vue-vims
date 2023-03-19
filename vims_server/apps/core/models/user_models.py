from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for vims.
    """

    #: First and last name do not cover global name patterns
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField(blank=True, max_length=255)
