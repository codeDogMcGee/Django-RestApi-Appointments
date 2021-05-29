from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy

class CustomUserManager(BaseUserManager):
    """
    CustomUser uses the email as unique 
    identifier rather than username.
    """
    def create_user(self, phone, email, name, password, **extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('Email is required.'))
        if not phone:
            raise ValueError(ugettext_lazy('Phone is required.'))
        if not name:
            raise ValueError(ugettext_lazy('Name is required.'))
        phone = phone
        email = self.normalize_email(email)
        name = name
        user = self.model(phone=phone, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        email = 'admin@admin.com'
        name = 'Admin'

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser mush have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser mush have is_superuser=True'))
        return self.create_user(phone, email, name, password, **extra_fields)