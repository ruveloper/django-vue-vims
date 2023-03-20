from django.conf import settings

from .api_requests import post


def validate_recaptcha_token(token: str) -> bool:
    """
    Validate reCaptcha v3 token
    :param token: (str) g_recaptcha_response token from post
    :return: validation: (bool) validation result
    """
    if settings.DEBUG:
        return True

    private_key = settings.RECAPTCHA_PRIVATE_KEY
    required_score = settings.RECAPTCHA_REQUIRED_SCORE

    # Send a post request to google recaptcha api to validate
    # https://developers.google.com/recaptcha/docs/verify
    data = {"secret": private_key, "response": token}
    response = post("https://www.google.com/recaptcha/api/siteverify", data=data)
    if not response:
        return False

    response_json: dict = response.json()
    success = response_json.get("success", False)
    score = response_json.get("score", 0.0)

    if not success or score < required_score:
        return False

    return True
