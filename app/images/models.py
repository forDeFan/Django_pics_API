from django.db import models


def user_dir_path(instance, filename: str) -> str:
    """
    Customized path to upload images to.
    Creates catalogue based on user 'id' value to upload images/ thumbnails in there.
    'owner' attribute relates to field 'owner' in Image model.
    """
    return "images/{0}/{1}".format(instance.owner.id, filename)


class Image(models.Model):
    """
    Image model class.
    """

    name = models.CharField(max_length=100, unique=False)
    # core.User to avoid circular import error
    owner = models.ForeignKey("core.User", on_delete=models.CASCADE, editable=False)
    image_link = models.ImageField(
        upload_to=user_dir_path, unique=False
    )
    thumbnail_small = models.CharField(
        max_length=255, null=True, blank=True
    )
    thumbnail_large = models.CharField(
        max_length=255, null=True, blank=True
    )
    expiring_link = models.CharField(
        max_length=255, null=True, blank=True
    )


class Tier(models.Model):
    """
    Tier model class.
    """

    name = models.CharField(max_length=100, default="Basic")
    image_link = models.BooleanField(default=False)
    thumbnail_small = models.BooleanField(default=True)
    thumbnail_large = models.BooleanField(default=True)
    expiring_link = models.BooleanField(default=True)

    def __str__(self) -> str:
        """
        Returns name value in str representation of the Tier object.
        """
        return "%s %s" % (self.name, "")
