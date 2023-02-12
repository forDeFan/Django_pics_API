import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ["basic", "premium", "enterprise", "custom_plan"]
MODELS = ["user"]
PERMISSIONS = ["custom"]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = "Can {} {}".format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(
                            name=name
                        )
                    except Permission.DoesNotExist:
                        logging.warning(
                            "Permission not found with name '{}'.".format(
                                name
                            )
                        )
                        continue

                    new_group.permissions.add(model_add_perm)
