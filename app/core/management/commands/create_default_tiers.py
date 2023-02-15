""" 
Command to create starting tiers.
"""

from django.core.management.base import BaseCommand
from images.models import Tier

TIERS = ["Basic", "Premium", "Enterprise"]


class Command(BaseCommand):
    def _create_basic_tiers(self):
        for tier in TIERS:
            t = Tier(name=tier)
            t.save()

    def handle(self, *args, **options):
        self._create_basic_tiers()
