from django.core.exceptions import ValidationError
from api.utils.static_vars import CATEGORIES


def validate(category):
    if category not in CATEGORIES:
        raise ValidationError('Menu category %(category)s is not valid. %(categories)s', params={'category': category, 'categories': CATEGORIES})
