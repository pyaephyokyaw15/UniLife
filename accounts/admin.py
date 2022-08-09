from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {
            'classes': ('wide',),
            'fields': ('profile_picture', 'followers')}
         ),
    )

# Register your models here.
admin.site.register(User, CustomAdmin)

