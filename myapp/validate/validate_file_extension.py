import os
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', 'jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Image upload only jpeg, jpg and png formate ')


def file_size(value):
    limit = 0.5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Maximum file size allowed is 500kb')
