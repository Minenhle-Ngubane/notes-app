from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the User model.
    """
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "gender",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (_("Authentication"), {"fields": ("email", "password")}),
        (_("Personal Info"), {
            "fields": (
                "first_name", 
                "last_name", 
                "gender", 
                "avatar",
            )
        }),
        (_("Permissions"), {
            "fields": (
                "is_active", 
                "is_staff", 
                "is_superuser", 
                "groups", 
                "user_permissions",
            )
        }),
        (_("Important Dates"), {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "gender",
                    "avatar",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    readonly_fields = ("date_joined",)
    filter_horizontal = ("groups", "user_permissions")