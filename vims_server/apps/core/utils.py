import os
from uuid import uuid4


def media_user_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4().hex}{ext}"
    user_id = (
        instance.user.id if hasattr(instance, "user") else instance.user_data.user.id
    )
    return os.path.join("users", str(user_id), filename)
