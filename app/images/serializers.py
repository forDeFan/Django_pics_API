from django.db import models
from images.models import Image, Tier
from rest_framework import serializers


class BasicTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image class for user in Basic Tier plan."""

    image_path = models.FileField(blank=False, null=False)

    class Meta:
        model = Image
        fields = ("id", "image_link", "thumbnail_small")


class PremiumTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image class for user in Premium Tier plan."""

    image_path = models.FileField(blank=False, null=False)

    class Meta:
        model = Image
        fields = (
            "id",
            "image_link",
            "thumbnail_small",
            "thumbnail_large",
        )


class EnterpriseTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image class for user in Enterprise Tier plan."""

    image_path = models.FileField(blank=False, null=False)

    class Meta:
        model = Image
        fields = (
            "id",
            "image_link",
            "thumbnail_small",
            "thumbnail_large",
            "expiring_link",
        )


class TierSerializer(serializers.ModelSerializer):
    """Serializer of Tier class."""

    class Meta:
        model = Tier
        fields = "__all__"


"""
POC

from rest_framework import serializers

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

    def to_representation(self, instance):
        # Call the parent to_representation() method to get the default representation
        representation = super().to_representation(instance)
        
        # Check if the model is valid
        if instance.is_valid():
            # If valid, return a subset of the fields
            representation = {
                'field1': representation['field1'],
                'field2': representation['field2']
            }
        else:
            # If invalid, return a different subset of fields
            representation = {
                'field1': representation['field1'],
                'field3': representation['field3']
            }
        
        return representation
"""
