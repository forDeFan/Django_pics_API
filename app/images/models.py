from django.core.validators import FileExtensionValidator
from django.db import models
from model_utils.managers import InheritanceManager


def user_dir_path(instance: object, filename: str) -> str:
    """
    Customized path to upload images to.
    Creates catalogue based on user 'id' value to upload images.
    'owner.id' relates to 'owner' field in Image model.
    """
    return "images/{0}/{1}".format(instance.owner.id, filename)


class Image(models.Model):
    """
    Image model class.
    """

    # core.User to avoid circular import error
    # owner relates to user.id.
    owner = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, editable=False
    )
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
    expiring_link = models.CharField(
        max_length=255, null=True, blank=True
    )


class AbstractTier(models.Model):
    # Lib to get child class type
    objects = InheritanceManager()
    name = models.CharField(max_length=100)
    thumbnail_small_size = models.IntegerField(
        blank=False, default=200, editable=False
    )
    thumbnail_large_size = models.IntegerField(
        blank=False, default=200, editable=False
    )

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

    pass


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


class CustomTier(EnterpriseTier):
    """
    Custom tier model class.
    """

    pass


# Set thumbnail size to Premium tier
PremiumTier._meta.get_field("thumbnail_large_size").default = 400

# Set fields for Custom tier
CustomTier._meta.get_field("thumbnail_small_size").editable = True
CustomTier._meta.get_field("thumbnail_large_size").editable = True
CustomTier._meta.get_field("image_link").editable = True
CustomTier._meta.get_field("expiring_link").editable = True
