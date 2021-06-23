from django.contrib.auth.models import Group

DELETE_OLD_APPOINTEMENTS_EVERY_N_DAYS = 1
MAX_APPOINTMENT_AGE_DAYS = 5

GROUPS = ['Employees', 'Customers', 'Managers']


def get_or_create_groups() -> dict[int, object]:
    output = {}
    for group_name in GROUPS:
        group, created = Group.objects.get_or_create(name=group_name) # get_or_create() returns a tuple (group_object, created_bool)
        output[group.name] = group
    return output


def format_phone_number(phone_number: str) -> str:
    if len(phone_number) == 10:
        try:
            int(phone_number) # make sure it's all numbers
            return f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
        except:
            pass
    return phone_number

