""" 
Command to create basic tier.
"""

from django.core.management.base import BaseCommand
from images.models import Tier

class Command(BaseCommand):

    def _create_basic_tier(self):
        tier = Tier(name="Basic")
        tier.save()


    def handle(self, *args, **options):
        self._create_basic_tier()