from django.test import TestCase
from django.contrib.auth import get_user_model
from images.models import BasicTier


class ModelTests(TestCase):
    """Tests for user model."""

    def test_create_user_with_email_successful(self):
        """Test creating user with email successful."""

        bt = BasicTier(name="Basic")
        bt.save()

        email = "test@test.com"
        password = "testPass"
        tier = bt
        user = get_user_model().objects.create_user(
            email=email, password=password, tier=tier
        )

        self.assertEqual(user.email, email)
