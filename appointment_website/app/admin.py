from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # main view
    list_display = ('phone', 'name', 'group', 'last_appointment_datetime', 'created', 'is_staff', 'is_active')
    list_filter = ('phone', 'name', 'group', 'last_appointment_datetime', 'created', 'is_staff', 'is_active')

    # user detail view
    fieldsets = (
        (None, {'fields': ('phone', 'name', 'last_appointment_datetime')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'group')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'group','password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ('phone', 'name', 'group')
    ordering = ('group', 'name', 'last_appointment_datetime', 'created')

admin.site.register(CustomUser, CustomUserAdmin)
