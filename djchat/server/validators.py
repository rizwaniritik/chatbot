from rest_framework.exceptions import ValidationError
from PIL import Image
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimesions for image are 70x70 - size of image you uploaded: {img.size()}"
                )


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", '.png', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}")