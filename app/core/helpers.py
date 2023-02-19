from django.core.exceptions import ValidationError
from PIL import Image as pil_img  # To avoid namespace conflicts
from rest_framework.request import Request


def user_dir_path(instance: object, filename: str) -> str:
    """
    Helper function to customize upload catalogue and path based 
    on user 'id' value.
    
    Returns: path to user id numered catalogue to upload files to.
    """
    return "images/{0}/{1}".format(instance.owner.id, filename)


def validate_number_range(value):
    """ 
    Helper function for int validation with range.
    """
    if value in range(300, 30000):
        return value
    raise ValidationError(
        "Number of seconds for expiring link should be in range of 300 - 30000"
    )

def make_binary(req: Request, inst_img_path: object) -> str:
    """ 
    Helper function to make binary image out of input image.

    Returns: 
        str: absolute image url path.
    """
    img_path = inst_img_path
    col = pil_img.open(img_path)
    # To gray scale
    gray = col.convert("L")  
    # Binarization
    bw = gray.point(
        lambda x: 0 if x < 128 else 255, "1"
    )

    bw_path = f"{img_path.split('.')[0]}-binary.jpg"
    bw.save(bw_path)
    abs_url = req.get_host() + bw_path.replace("/app", "")

    return abs_url


def make_thumbnail(
    req: Request,
    size: int,
    inst_img_path: object,
    thumb_name: str,
) -> str:

    """
    Helper function to produce thumbnail of desired size from uploaded image.

    Returns:
        str: absolute url path to uploaded image
    """
    img_path = inst_img_path
    host_addres = req.get_host()
    thumb_size = (size*2, size)

    im = pil_img.open(img_path)
    im.thumbnail(thumb_size)
    thumb_path = f"{img_path.split('.')[0]}-{thumb_name}.jpg"
    im.save(thumb_path)

    abs_url = host_addres + thumb_path.replace("/app", "")
    return abs_url
