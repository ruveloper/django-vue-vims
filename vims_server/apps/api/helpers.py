from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from apps.services import validate_recaptcha_token


def validate_recaptcha_form(request: Request) -> None:
    """
    Validate reCaptcha form submit raising ValidationError on fail.
    :param request: (Request) rest framework Request instance
    """
    token = request.data.get("g-recaptcha-response", None)
    if not token:
        raise ValidationError({"non_field_errors": ["reCaptcha missing token"]})
    validation = validate_recaptcha_token(token)
    if not validation:
        raise ValidationError({"non_field_errors": ["reCaptcha invalid Token"]})
    return None
