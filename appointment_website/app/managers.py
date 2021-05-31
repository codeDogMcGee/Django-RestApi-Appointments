from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    CustomUser uses the email as unique 
    identifier rather than username.
    """
    def create_user(self, phone, email, name, group, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required.'))
        if not phone:
            raise ValueError(_('Phone is required.'))
        if not name:
            raise ValueError(_('Name is required.'))

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
            raise ValueError(_('Superuser mush have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser mush have is_superuser=True'))

        superuser = self.model(phone=phone, **extra_fields)
        superuser.set_password(password)
        superuser.save()

        return superuser
