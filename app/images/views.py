from images.models import Image
from images.serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated


class ImageCreateView(viewsets.ModelViewSet):
    """
    API view to upload image.
    """

    parser_classes = (MultiPartParser,)
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_groups = [group.name for group in user.groups.all()]

        if "basic" in user_groups:
            thumbnail_size = (200, 200)
        else:
            thumbnail_size = (500, 500)

        image = serializer.save(owner=user)
        image_path = image.image.path

        from PIL import Image

        im = Image.open(image_path)
        im.thumbnail(thumbnail_size)
        im.save(f"thumbnail_{image.name}.jpg")


class ImageListView(viewsets.ModelViewSet):
    """
    API view to retrieve list of all images uploaded by
    a specific user.
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return list of all images owned by a user."""
        user = self.request.user
        return Image.objects.filter(owner=user)
