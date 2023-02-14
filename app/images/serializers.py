import os

from django.db import models
from images.models import Image
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class ImageSerializer(serializers.ModelSerializer):
    image_path = models.FileField(blank=False, null=False)

    class Meta:
        model = Image
        fields = ("name", "image", "owner")

        def create(self, validated_data):
            images = validated_data.pop('image')
            owner = validated_data.pop('owner')
            for image in images:
                Image.objects.create(owner=owner, image=image)
            return validated_data

