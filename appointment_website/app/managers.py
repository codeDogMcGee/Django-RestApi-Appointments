from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy


# employee_group, employee_group_created = Group.objects.get_or_create(name='Employees')
# customer_group, customer_group_created = Group.objects.get_or_create(name='Customers')
# def get_group():
#     employee_group, employee_group_created = Group.objects.get_or_create(name='Employees')
#     customer_group, customer_group_created = Group.objects.get_or_create(name='Customers')

#     # get the content type from the model to use in permissions
#     # content_type = ContentType.objects.get_for_model(CustomUser)
#     # employee_permission = Permission.objects.create(codename='can_create_user',
#     #                                                 name='Can add user',
#     #                                                 content_type=content_type)
#     # employee_group.permissions.add(employee_permission)

def get_user_to_groups(include_admin=False):
    output = {}
    if include_admin:
        admin_group, admin_group_created = Group.objects.get_or_create(name='Admin')
        output['admin_group'] = admin_group

    employee_group, employee_group_created = Group.objects.get_or_create(name='Employees')
    customer_group, customer_group_created = Group.objects.get_or_create(name='Customers')

    output['employee_group'] = employee_group
    output['customer_group'] = customer_group

    return output


class CustomUserManager(BaseUserManager):
    """
    CustomUser uses the email as unique 
    identifier rather than username.
    """
    def create_user(self, phone, email, name, group, password, **extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('Email is required.'))
        if not phone:
            raise ValueError(ugettext_lazy('Phone is required.'))
        if not name:
            raise ValueError(ugettext_lazy('Name is required.'))

        phone = phone
        email = self.normalize_email(email)
        name = name
        group = group
        
        user = self.model(phone=phone, email=email, name=name, group=group, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser mush have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser mush have is_superuser=True'))

        superuser = self.model(phone=phone, **extra_fields)
        superuser.set_password(password)
        superuser.save()

        return superuser
