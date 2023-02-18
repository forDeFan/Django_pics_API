""" 
Command to create starting tiers.
"""

from django.core.management.base import BaseCommand
from images.models import BasicTier, PremiumTier, EnterpriseTier


class Command(BaseCommand):
    def _create_basic_tiers(self):
        bt = BasicTier(name="Basic")
        bt.save()
        pt = PremiumTier(name="Premium")
        pt.save()
        et = EnterpriseTier(name="Enterprise")
        et.save()

    def handle(self, *args, **options):
        self._create_basic_tiers()
