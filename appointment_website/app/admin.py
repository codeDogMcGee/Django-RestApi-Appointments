from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('phone', 'email', 'name', 'is_staff', 'is_active',)
    list_filter = ('phone', 'email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('phone', 'email', 'name',)
    ordering = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)
