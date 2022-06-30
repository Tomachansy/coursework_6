from phonenumber_field import serializerfields
from rest_framework import serializers

from ads.models import Comment, Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["pk", "title", "price", "description", "image"]


class AdDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source="author.id")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    phone = serializerfields.PhoneNumberField(source="author.phone", read_only=True)

    class Meta:
        model = Ad
        fields = ["pk", "title", "price", "description", "author_id", "author_first_name", "author_last_name", "phone", "image"]


class CommentSerializer(serializers.ModelSerializer):
    ad_id = serializers.ReadOnlyField(source="ad.id", read_only=True)
    author_id = serializers.ReadOnlyField(source="author.id")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_image = serializers.ImageField(source="author.image", read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "text", "created_at", "ad_id", "author_id", "author_first_name", "author_last_name", "author_image"]

