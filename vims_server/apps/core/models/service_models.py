from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Service(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    SERVICE_CHOICES = [
        ("pexels", "Pexels"),
        ("unsplash", "Unsplash"),
        ("pixabay", "Pixabay"),
    ]
    service = models.CharField(
        max_length=20,
        choices=SERVICE_CHOICES,
        default=SERVICE_CHOICES[0][0],
        unique=True,
    )
    api_endpoint = models.URLField(max_length=255, unique=True)
    APIKEY_TYPE_CHOICE = [
        ("header", "Header"),
        ("query", "Query Parameter"),
    ]
    apikey_type = models.CharField(
        max_length=20, choices=APIKEY_TYPE_CHOICE, default=APIKEY_TYPE_CHOICE[0][0]
    )
    apikey = models.CharField(max_length=255, help_text="Set the new api key")
    per_page_default = models.IntegerField(
        default=10, validators=[MinValueValidator(5), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.service

    class Meta:
        ordering = ["service"]
