from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('last_updated',)}),
    )
    readonly_fields = ('last_updated',)

admin.site.register(CustomUser, CustomUserAdmin)
