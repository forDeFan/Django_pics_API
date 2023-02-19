from core.helpers import make_binary, make_thumbnail
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
        # For swagger api docs UI - when anonymous user, before authorize
        return BasicTierImageSerializer


class ImageCreateView(viewsets.ModelViewSet):
    """
    API view for image uploading.
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
        Creates and save image object.
        Returns Response with serialized fields to the app user.
        """

        req_user = self.request.user
        # Image object
        instance = serializer.save(owner=req_user)

        # Links
        image_path = instance.image_link.path
        image_link = str(image_path).replace("/app/media", "")

        # Thumbnail sizes
        small_thumb_size = req_user.tier.thumbnail_small_size
        large_thumb_size = req_user.tier.thumbnail_large_size

        # Expiring link empty val if not Enetrprise or Custom tier
        expiring_link = ""

        tier_type = get_tier_type(req=self.request)

        # Make image binary in expiring link for Enterprise and Custom tiers.
        if (tier_type.__name__).__eq__(CustomTier.__name__) or (
            tier_type.__name__
        ).__eq__(EnterpriseTier.__name__):

            small_thumb_size = req_user.tier.thumbnail_small_size
            large_thumb_size = req_user.tier.thumbnail_large_size
            image_link = image_link

            tier = BasicTier.objects.filter(
                name=req_user.tier.name
            ).select_subclasses()

            # If attachment of link in True in tier.expiring_link
            for t in tier:
                if(t.expiring_link):
                    expiring_link = make_binary(
                        req=self.request, inst_img_path=image_path
                    )  

        # Make thumbnails
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
        instance.expiring_link = expiring_link
        # Bit of hacking here - django throws UTF rncoding errors when
        # serializer.to_representation tryed to reach native image url.
        instance.image_link = image_link

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
