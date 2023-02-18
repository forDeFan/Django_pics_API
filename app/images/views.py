from django.db.models.query import QuerySet
from images.models import (
    BasicTier,
    CustomTier,
    EnterpriseTier,
    Image,
    PremiumTier,
)
from images.serializers import (
    BasicTierImageSerializer,
    CustomTierImageSerializer,
    EnterpriseTierImageSerializer,
    PremiumTierImageSerializer,
)
from PIL import Image as pil_img  # To avoid namespace conflicts
from rest_framework import serializers, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


def get_tier_type(req: Request) -> type[BasicTier]:
    """
    Helper function to return BasicTier child class type.
    Uses InheritanceManager from AbstractTier class.

    Returns: type of tier class
    """
    tier = BasicTier.objects.filter(
        name=req.user.tier.name
    ).select_subclasses()

    for t in tier:
        return type(t)
    

def get_serializer(req: Request) -> serializers.ModelSerializer:
        """
        Helper function to set up serializer class in relation to request 
        user Tier plan.

        Returns:
            ModelSerializer: reference to appriopriate serializer
        """
        try:
            tier_type = get_tier_type(req=req)

            if tier_type == PremiumTier:
                return PremiumTierImageSerializer
            if tier_type == EnterpriseTier:
                return EnterpriseTierImageSerializer
            if tier_type == CustomTier:
                return CustomTierImageSerializer
            return BasicTierImageSerializer
        except:
            return BasicTierImageSerializer



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
        thumb_size = (size, size)

        im = pil_img.open(img_path)
        im.thumbnail(thumb_size)
        thumb_path = f"{img_path.split('.')[0]}-{thumb_name}.jpg"
        im.save(thumb_path)

        abs_url = host_addres + thumb_path.replace("/app", "")
        return abs_url

class ImageCreateView(viewsets.ModelViewSet):
    """
    API view to upload image.
    """

    parser_classes = (MultiPartParser,)
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """
        Set up serializer class in relation to request user Tier plan.

        Returns:
            ModelSerializer: reference to appriopriate serializer
        """
        return get_serializer(req=self.request)


    def perform_create(self, serializer):
        """
        Create object in db along with all model fields.
        """

        req_user = self.request.user
        instance = serializer.save(owner=req_user)

        image_path = instance.image_link.path
        image_link = str(image_path).replace("/app/media", "")

        small_thumb_size = req_user.tier.thumbnail_small_size
        large_thumb_size = req_user.tier.thumbnail_large_size

        expiring_link = "expiring link"

        tier_type = get_tier_type(req=self.request)

        if tier_type == CustomTier or EnterpriseTier:
            small_thumb_size = req_user.tier.thumbnail_small_size
            large_thumb_size = req_user.tier.thumbnail_large_size
            image_link = image_link
            expiring_link = "expiring link"

        small_thumb = make_thumbnail(
            req=self.request,
            size=small_thumb_size,
            inst_img_path=image_path,
            thumb_name="thumb-small",
        )

        large_thumb = make_thumbnail(
            req=self.request,
            size=large_thumb_size,
            inst_img_path=image_path,
            thumb_name="thumb-large",
        )

        # Populate instance fields
        instance.thumbnail_small = small_thumb
        instance.thumbnail_large = large_thumb
        # Bit of hacking here - django throws UTF rncoding errors when
        # serializer.to_representation tryed to reach native image url.
        instance.image_link = image_link
        instance.expiring_link = expiring_link

        # Save instance
        instance.save()


class ImageListView(viewsets.ModelViewSet):
    """
    API view to retrieve list of all images uploaded by
    a specific user
    """

    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """
        Set up serializer class in relation to request user Tier plan.

        Returns:
            ModelSerializer: reference to appriopriate serializer
        """
        return get_serializer(req=self.request)


    def get_queryset(self) -> QuerySet:
        """
        Return list of all images owned by user - in his current tier plan.
        Plan can be changed during user lifetime span and appriopiate field set
        will be returned in relation to that currently selected user plan.
        """
        req_user = self.request.user

        return Image.objects.filter(owner=req_user)
