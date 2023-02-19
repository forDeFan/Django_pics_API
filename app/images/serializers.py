from images.models import Image
from rest_framework import serializers


class BasicTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in user Basic Tier plan."""

    class Meta:
        model = Image
        # Expiring second for swagger UI - to be visible in other plans
        fields = ["image_link"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["image_link"] = ""
        representation["thumbnail_small"] = instance.thumbnail_small

        return representation


class PremiumTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in Premium Tier plan."""

    class Meta:
        model = Image
        fields = ["image_link"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = instance.thumbnail_large

        return representation


class EnterpriseTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in Enterprise Tier plan."""

    class Meta:
        model = Image
        fields = ["image_link"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = instance.thumbnail_large
        representation["expiring_link"] = instance.expiring_link

        return representation


class CustomTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in Custom Tier plan."""

    class Meta:
        model = Image
        fields = ["image_link"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = instance.thumbnail_large
        representation["expiring_link"] = instance.expiring_link

        return representation

