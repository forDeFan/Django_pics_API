"""
Test for Django custom command for Tiers creation.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase

@patch("core.management.commands.create_default_tiers.Command._create_basic_tiers")
class CommandTests(SimpleTestCase):

    def test_create_basic_tiers_started(self, patched_create):
        """ 
        Test if command called.
        """

        patched_create.return_value = None

        call_command("create_default_tiers")

        patched_create.assert_called_once


class CommandTestWithTiers(SimpleTestCase):

    @patch("images.models.BasicTier.save")
    def test_tiers_created(self, patched_save):
        """ 
        Test if save called on tier instance.
        """

        patched_save.return_value = True

        call_command("create_default_tiers")

        self.assertEqual(patched_save.call_count, 3)

    