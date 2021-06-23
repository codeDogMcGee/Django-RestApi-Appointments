from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ApiUserCreationForm, ApiUserChangeForm
from .models import ApiUser


class CustomUserAdmin(UserAdmin):
    add_form = ApiUserCreationForm
    form = ApiUserChangeForm
    model = ApiUser

    # main view
    list_display = ('phone', 'name', 'last_appointment_datetime', 'created', 'is_staff', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_active', 'last_appointment_datetime', 'created') # 'phone', 'name',

    # user detail view
    fieldsets = (
        (None, {'fields': ('phone', 'name', 'last_appointment_datetime')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'groups','password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ('phone', 'name', 'groups')
    ordering = ('groups', 'name', 'last_appointment_datetime', 'created')

admin.site.register(ApiUser, CustomUserAdmin)