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


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = models.Comments
        fields = ("description", "user", "created_at")


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagsSerializer(many=True)
    post = CommentSerializer(many=True, read_only=True)
    author = ProfileSerializer()

    class Meta:
        model = models.Posts
        fields = ("title", "image", "description", "category", "author", "tags", "watched", "created_at", "post")

    def create(self, validate_data):
        tags_data = validate_data.pop("tags")
        category_data = validate_data.pop("category")
        category, created = models.Category.objects.get_or_create(**category_data)
        post = models.Posts.objects.create(category=category, **validate_data)
        for tag in tags_data:
            tag, created = models.Tags.objects.get_or_create(**tags_data)
            post.tags.add(tag)
        return post


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.name")

    class Meta:
        model = models.Posts
        fields = ("title", "description", "image", "category", "tags", "author")
