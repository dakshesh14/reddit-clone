from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_admin']
    list_filter = ('is_admin',)


admin.site.register(User, CustomUserAdmin)
