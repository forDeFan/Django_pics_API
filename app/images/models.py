from django.db import models


def user_dir_path(instance, filename: str) -> str:
    """ 
    Customized path to upload images to.
    """
    return "images/{0}".format(filename)


class Image(models.Model):
    """
    Image model class.
    """
    name = models.CharField(max_length=100)
    # core.User to avoid circular import error
    owner = models.ForeignKey("core.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_dir_path)

    class Meta:
        """ 
        Make possible for user to keep multiple images ownership
        associated to his id.
        """
        unique_together = ('owner', 'image')


