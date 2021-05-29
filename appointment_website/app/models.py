from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .validators import validate_is_int

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('phone number'), max_length=10, 
                             validators=[MinLengthValidator(10), validate_is_int],
                             unique=True, blank=False)
    email = models.EmailField(_('email address'), blank=False)
    name = models.CharField(_('name'), max_length=100, blank=False)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # Require 'email', 'name' in production

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} | {self.phone} | {self.email}| {self.group}'


