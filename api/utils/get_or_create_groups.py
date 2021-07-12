from django.contrib.auth.models import Group

from api.utils.static_vars import GROUPS
from api.utils.create_group_id_object import create_group_id_object
from api.models import ApiUser


def get_or_create_groups() -> dict[str, object]:
    output = {}
    
    for group_name in GROUPS:
        group, created = Group.objects.get_or_create(name=group_name) # get_or_create() returns a tuple (group_object, created_bool)
        output[group.name] = group

        # if the group is new add it to the GroupIdsModel
        if created:
            create_group_id_object(group)

            if group.name == 'Admins':
                superusers = ApiUser.objects.filter(is_superuser=True)
                for su in superusers:
                    group.user_set.add(su)


    return output  # {group_name: group, ...}