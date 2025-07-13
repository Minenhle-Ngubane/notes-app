import os
import uuid
from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uuid.uuid4(), filename=filename, ext=ext
        ),
    )


def validate_avatar(image):
    """
    Validate avatar image for size and format.
    """
    # Check file size (max 2MB)
    max_size = 2 * 1024 * 1024  # 2MB in bytes
    if image.size > max_size:
        raise ValidationError(_("Image file size cannot exceed 2MB."))
    
    # Check file format
    allowed_formats = ["JPEG", "JPG", "PNG"]
    try:
        with Image.open(image) as img:
            if img.format not in allowed_formats:
                raise ValidationError(_("Only JPG and PNG image formats are allowed."))
    except Exception:
        raise ValidationError(_("Invalid image file."))