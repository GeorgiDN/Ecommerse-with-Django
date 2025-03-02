from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ecommerseApp.accounts.models import CustomUser, Customer


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
