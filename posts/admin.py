from django.contrib import admin

from .models import Post, PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Inline(admin.TabularInline):
        model = PostImage

    inlines = [Inline, ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
