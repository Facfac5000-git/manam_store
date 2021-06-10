from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User


class UserAdmin(UserAdmin):
    list_display = ['username']


admin.site.register(User, UserAdmin)
