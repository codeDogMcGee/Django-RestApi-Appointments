from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ApiUserCreationForm, ApiUserChangeForm
from .models import ApiUser


class CustomUserAdmin(UserAdmin):
    add_form = ApiUserCreationForm
    form = ApiUserChangeForm
    model = ApiUser

    # main view
    list_display = ('email', 'name', 'phone', 'last_appointment_datetime', 'created', 'is_staff', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_active', 'last_appointment_datetime', 'created')

    # user detail view
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'last_appointment_datetime')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'groups','password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ('email', 'name', 'phone', 'groups')
    ordering = ('groups', 'name', 'last_appointment_datetime', 'created')

admin.site.register(ApiUser, CustomUserAdmin)