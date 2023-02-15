from images.models import Image
from images.serializers import (
    BasicTierImageSerializer,
    EnterpriseTierImageSerializer,
    PremiumTierImageSerializer,
)
from PIL import Image as pil_img  # To avoid namespace conflicts
from rest_framework import serializers, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated


class ImageCreateView(viewsets.ModelViewSet):
    """
    API view to upload image.
    """

    parser_classes = (MultiPartParser,)
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Set up serializer class in relation to user Tier plan."""
        try:
            if self.request.user.tier.name == "premium" or "Premium":
                return PremiumTierImageSerializer
            if (
                self.request.user.tier.name == "enterprise"
                or "Enterprise"
            ):
                return EnterpriseTierImageSerializer
            return BasicTierImageSerializer
        except:
            return BasicTierImageSerializer

    def perform_create(self, serializer):

        user = self.request.user
        user_tier = user.tier.name

        # Save uploaded Image to instance
        instance = serializer.save(owner=user)
        # Get saved image path
        image_path = instance.image_link.path

        im = pil_img.open(image_path)

        if user_tier == "Basic":
            thumbnail_size = (200, 200)
            im.thumbnail(thumbnail_size)
            thumbnail_path = (
                f"{image_path.split('.')[0]}-small-thumbnail.jpg"
            )
            im.save(thumbnail_path)
            instance.image = thumbnail_path

        if user_tier == "Premium":
            thumbnail_size = (450, 450)
            im.thumbnail(thumbnail_size)
            thumbnail_path = (
                f"{image_path.split('.')[0]}-large-thumbnail.jpg"
            )
            im.save(thumbnail_path)
            instance.thumbnail_large = thumbnail_path
            instance.image_link = image_path

        # Save changes in Image instance
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
        Set up serializer class in relation to user Tier plan.
        Will return fields in Response - in relation to user plan.
        """
        try:
            if self.request.user.tier.name == "premium" or "Premium":
                return PremiumTierImageSerializer
            if (
                self.request.user.tier.name == "enterprise"
                or "Enterprise"
            ):
                return EnterpriseTierImageSerializer
            return BasicTierImageSerializer
        except:
            return BasicTierImageSerializer

    def get_queryset(self):
        """Return list of all images owned by user."""
        user = self.request.user
        return Image.objects.filter(owner=user)
