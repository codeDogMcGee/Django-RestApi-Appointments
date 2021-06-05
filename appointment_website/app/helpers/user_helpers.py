from app.models import CustomUser

def get_groups_for_user(user: CustomUser) -> list[str]:
    groups = []
    if user in CustomUser.objects.filter(group__name='Customers'): # if user in Customers group
        groups.append('Customers')
    elif user in CustomUser.objects.filter(group__name='Employees'): # if user in Employees group
        groups.append('Employees')
    return groups