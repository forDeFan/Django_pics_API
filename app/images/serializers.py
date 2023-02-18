from images.models import BasicTier, Image
from rest_framework import serializers


class BasicTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in user Basic Tier plan."""

    class Meta:
        model = Image
        fields = ("id", "owner", "image_link")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["image_link"] = ""
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = ""
        representation["expiring_link"] = ""

        return representation


class PremiumTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in Premium Tier plan."""

    class Meta:
        model = Image
        fields = ("id", "owner", "image_link")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = instance.thumbnail_large
        representation["expiring_link"] = ""

        return representation


class EnterpriseTierImageSerializer(serializers.ModelSerializer):
    """Serializer for Image in Enterprise Tier plan."""

    class Meta:
        model = Image
        fields = ("id", "owner", "image_link")

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
        fields = ("id", "owner", "image_link")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["thumbnail_small"] = instance.thumbnail_small
        representation["thumbnail_large"] = instance.thumbnail_large
        representation["expiring_link"] = instance.expiring_link

        return representation


class TierSerializer(serializers.ModelSerializer):
    """Serializer of Tier class."""

    class Meta:
        model = BasicTier
        fields = "__all__"
