from typing import List

from core import models as user_model
from images import models as image_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define users page in admin panel"""

    def tier(self, user) -> List:
        """If there will be more tiers in tge future."""
        tiers = []
        for tier in user.tier.all():
            tiers.append(tier.name)
        return " ".join(tiers)

    # Column name in admin UI.
    tier.short_description = "Tier"

    ordering = ["id"]

    list_display = [
        "id",
        "email",
        "name",
        "tier",
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
        (_("User tier"), {"fields": ("tier",)}),
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
                    "tier",
                ),
            },
        ),
    )

# Attach models to admin panel.
admin.site.register(user_model.User, UserAdmin)
admin.site.register(image_model.BasicTier)
admin.site.register(image_model.CustomTier)