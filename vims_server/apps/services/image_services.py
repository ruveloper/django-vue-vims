from dataclasses import dataclass
from urllib.parse import urljoin

from requests import Response

from apps.core.models import Service
from apps.services.api_requests import get


@dataclass
class ApiImage:
    service: str
    id: str
    link: str
    name: str
    preview_url: str
    original_url: str
    author: str


class PexelsApi:
    def __init__(self, service: Service):
        self.service = service

    def search(self, query: str, page: int = 1, per_page: int = None) -> list[ApiImage]:
        response: Response = get(
            url=urljoin(self.service.api_endpoint, "search"),
            params={
                "query": query,
                "page": page,
                "per_page": self.service.per_page_default if not per_page else per_page,
            },
            headers={"Authorization": self.service.apikey},
        )
        if not response:
            return []
        data = response.json()
        api_images: list[ApiImage] = []
        for image in data.get("photos", []):
            image_alt = image.get("alt", None)
            image_alt = image_alt if image_alt is not None else f"Image {image['id']}"
            image_name = image_alt[:20] + "..." if len(image_alt) > 20 else image_alt
            api_images.append(
                ApiImage(
                    self.service.service,
                    image["id"],
                    image["url"],
                    image_name,
                    image["src"]["medium"],
                    image["src"]["original"],
                    image["photographer"],
                )
            )
        return api_images


class UnsplashApi:
    def __init__(self, service: Service):
        self.service = service

    def search(self, query: str, page: int = 1, per_page: int = None) -> list[ApiImage]:
        response: Response = get(
            url=urljoin(self.service.api_endpoint, "search/photos"),
            params={
                "query": query,
                "page": page,
                "per_page": self.service.per_page_default if not per_page else per_page,
            },
            headers={"Authorization": f"Client-ID {self.service.apikey}"},
        )
        if not response:
            return []
        data = response.json()
        api_images: list[ApiImage] = []
        for image in data.get("results", []):
            image_alt = image.get("alt_description", None)
            image_alt = image_alt if image_alt is not None else f"Image {image['id']}"
            image_name = image_alt[:20] + "..." if len(image_alt) > 20 else image_alt
            api_images.append(
                ApiImage(
                    self.service.service,
                    image["id"],
                    image["links"]["html"],
                    image_name,
                    image["urls"]["small"],
                    image["urls"]["raw"],
                    image["user"]["name"],
                )
            )
        return api_images


class PixabayApi:
    def __init__(self, service: Service):
        self.service = service

    def search(self, query: str, page: int = 1, per_page: int = None) -> list[ApiImage]:
        response: Response = get(
            url=self.service.api_endpoint,
            params={
                "key": self.service.apikey,
                "q": query,
                "page": page,
                "per_page": self.service.per_page_default if not per_page else per_page,
            },
        )
        if not response:
            return []
        data = response.json()
        api_images: list[ApiImage] = []
        for image in data.get("hits", []):
            image_name = f"Image {image['id']}"
            api_images.append(
                ApiImage(
                    self.service.service,
                    image["id"],
                    image["pageURL"],
                    image_name,
                    image["webformatURL"],
                    image["largeImageURL"],
                    image["user"],
                )
            )
        return api_images
