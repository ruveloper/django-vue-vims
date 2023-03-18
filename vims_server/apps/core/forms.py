from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.forms.widgets import PasswordInput

from apps.core.models import Service

User = get_user_model()


class ServiceAddForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "apikey": PasswordInput,
        }


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """
    Form for User Update in the Admin Area.
    """

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": "This username has already been taken."}
        }
