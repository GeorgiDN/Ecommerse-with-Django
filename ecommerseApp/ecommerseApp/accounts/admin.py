from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ecommerseApp.accounts.models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class CustomerAdmin(admin.ModelAdmin):
    pass
