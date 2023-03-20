from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from apps.api.views import (
    ListServices,
    ReCaptcha,
    Registration,
    Search,
    TokenLogin,
    TokenLogout,
    UserDetail,
    UserFavoriteImageViewSet,
    UserImageViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("user/images", UserImageViewSet, basename="user_image")
router.register(
    "user/favorites", UserFavoriteImageViewSet, basename="user_favorite_image"
)

urlpatterns = [
    # * Docs URLs
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="api:api-schema"),
        name="api-docs",
    ),
    # * AUTH URLs
    # Login with token (Header "Authorization: Token <token>")
    path("auth/token/", TokenLogin.as_view(), name="token"),
    path("auth/logout/", TokenLogout.as_view(), name="logout"),
    path("auth/register/", Registration.as_view(), name="register"),
    # * URLs
    path("", include(router.urls)),
    # Public
    path("search/", Search.as_view(), name="search"),
    path("services/", ListServices.as_view(), name="services"),
    path("recaptcha/", ReCaptcha.as_view(), name="recaptcha"),
    # User
    path("user/details/", UserDetail.as_view(), name="user-detail"),
]
