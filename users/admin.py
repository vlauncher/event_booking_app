from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user", "address", "phone_number")
    list_filter = ("user", "address", "phone_number")
    search_fields = ("user", "address", "phone_number")
    ordering = ("user", "address", "phone_number")

    fieldsets = ((None, {"fields": ("user", "address", "phone_number")}),)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("user", "address", "phone_number"),
            },
        ),
    )
