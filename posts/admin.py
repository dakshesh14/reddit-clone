from django.contrib import admin

from .models import Community, JoinedCommunity, Post, PostImage


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(JoinedCommunity)
class JoinedCommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Inline(admin.TabularInline):
        model = PostImage

    inlines = [Inline, ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
