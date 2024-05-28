from rest_framework import serializers
from blog import models
from users.api.serializers import ProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("title",)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ("title",)


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagsSerializer(many=True)
    author = ProfileSerializer()

    class Meta:
        model = models.Posts
        fields = ("title", "image", "description", "category", "author", "tags", "watched", "created_at",)


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.name")

    class Meta:
        model = models.Posts
        fields = ("title", "description", "image", "category", "tags", "author")


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comments
        fields = ("description", "user", "post", "created_at")


class CommentListSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    post = PostSerializer()

    class Meta:
        model = models.Comments
        fields = ("description", "user", "post", "created_at")
