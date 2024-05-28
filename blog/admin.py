from django.contrib import admin
from blog import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(models.Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "is_published", "created_at", "updated_at")
    list_editable = ("is_published",)


admin.site.register(models.Comments)
