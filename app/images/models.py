from django.core.validators import FileExtensionValidator
from django.db import models
from model_utils.managers import InheritanceManager
from django.utils import timezone
from core.helpers import user_dir_path, validate_number_range


class Image(models.Model):
    """
    Image model class.
    """

    # core.User to avoid circular import error
    # owner relates to user.id.
    owner = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, editable=False
    )
    created = models.DateTimeField(default=timezone.now)
    thumbnail_small = models.CharField(
        max_length=255, null=True, blank=True
    )
    thumbnail_large = models.CharField(
        max_length=255, null=True, blank=True
    )
    image_link = models.ImageField(
        upload_to=user_dir_path,
        unique=False,
        validators=[FileExtensionValidator(["jpg", "png"])],
    )
    seconds = models.IntegerField(
        validators=[validate_number_range], default=300
    )
    expiring_link = models.CharField(
        max_length=255, null=True, blank=True
    )


class AbstractTier(models.Model):
    # Lib to get child class type
    objects = InheritanceManager()
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """
        Returns name value in str representation of the Tier object.
        """
        return "%s %s" % (self.name, "")


class BasicTier(AbstractTier):
    """
    Basic tier model class.
    """

    thumbnail_small_size = models.IntegerField(
        blank=True, default=200, editable=False
    )
    thumbnail_large_size = models.IntegerField(
        blank=True, default=400, editable=False
    )


class PremiumTier(BasicTier):
    """
    Premium tier model class.
    """

    image_link = models.BooleanField(default=True, editable=False)


class EnterpriseTier(PremiumTier):
    """
    Enterprise tier model class.
    """

    expiring_link = models.BooleanField(default=True, editable=False)


class CustomTier(BasicTier):
    """
    Custom tier model class.
    """
    
    image_link = models.BooleanField(default=True, editable=True)
    expiring_link = models.BooleanField(default=True, editable=True)
