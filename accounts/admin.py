from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Add 'profile_picture and followers' fields on users when accessing via Django Admin dashboard
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {
            'classes': ('wide',),
            'fields': ('profile_picture', 'followers')}
         ),
    )


# Register your models here.
admin.site.register(User, CustomUserAdmin)

