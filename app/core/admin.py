from core import models
from typing import List
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission


class UserAdmin(BaseUserAdmin):
    """Define users page in admin panel"""

    def group(self, user) -> List:
        """
        Custom listing implementation to show user group in
        admin UI.
        """
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return " ".join(groups)

    # Column name in admin UI.
    group.short_description = "Group"

    ordering = ["id"]

    list_display = [
        "email",
        "name",
        "group",
        "is_active",
        "is_superuser",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("User groups"), {"fields": ("groups",)}),
    )

    readonly_fields = ["last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
