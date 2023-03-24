from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from apps.core.forms import ServiceAddForm, UserAdminChangeForm, UserAdminCreationForm
from apps.core.models import Service, UserData, UserFavoriteImage, UserImage

User = get_user_model()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAddForm


class UserImageInline(admin.TabularInline):
    model = UserImage
    fields = ("pk", "name", "image")
    readonly_fields = ("pk",)
    extra = 0


class UserFavoriteImageInline(admin.StackedInline):
    model = UserFavoriteImage
    fields = (
        "pk",
        "service",
        "image_id",
        "author",
        "name",
        "link",
        "preview_url",
        "original_url",
    )
    readonly_fields = ("pk",)
    extra = 0


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    readonly_fields = ("max_user_images", "max_user_favorites")
    inlines = [
        UserImageInline,
        UserFavoriteImageInline,
    ]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

    # inlines = [UserImageInline, ]
