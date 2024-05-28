from django.db import models
from utils.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Tags(BaseModel):
    title = models.CharField(max_length=129, unique=True)

    def __str__(self):
        return self.title


class Posts(BaseModel):
    title = models.CharField(max_length=128)
    description = models.TextField()

    image = models.ImageField(upload_to="posts/")
    watched = models.IntegerField(default=0, editable=False)

    is_published = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    tags = models.ManyToManyField(Tags, related_name="tags")
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="author")

    def __str__(self):
        return self.title


class Comments(BaseModel):
    description = models.TextField()

    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="viewer")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post")

    def __str__(self):
        return self.user.name
