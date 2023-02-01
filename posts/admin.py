from django.contrib import admin

from .models import (
    Post,
    PostImage,
    PostVote,
    PostShare,
    Comment,
    CommentVote,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Inline(admin.TabularInline):
        model = PostImage

    inlines = [Inline, ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    pass


@admin.register(PostShare)
class PostShareAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    pass
