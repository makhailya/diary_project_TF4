from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('bio', 'avatar')
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'date_joined')
