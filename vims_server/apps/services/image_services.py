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
        data = response.json()
        api_images: list[ApiImage] = []
        for image in data.get("photos", []):
            image_name = (
                image["alt"][:20] + "..." if len(image["alt"]) > 20 else image["alt"]
            )
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
        data = response.json()
        api_images: list[ApiImage] = []
        for image in data.get("results", []):
            image_name = (
                image["alt_description"][:20] + "..."
                if len(image["alt_description"]) > 20
                else image["alt_description"]
            )
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
                "query": query,
                "page": page,
                "per_page": self.service.per_page_default if not per_page else per_page,
            },
        )
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