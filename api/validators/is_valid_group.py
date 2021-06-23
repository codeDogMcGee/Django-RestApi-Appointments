from django.core.exceptions import ValidationError

from api.utils.static_vars import GROUPS

def validate(group_name):
    group_name = group_name.lower()
    group_name = group_name[0].upper() + group_name[1:]
    if group_name not in GROUPS:
        raise ValidationError('%(group_name)s is not a valid group.', params={'group_name': group_name})
    return group_name