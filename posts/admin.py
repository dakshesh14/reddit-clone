from django.contrib import admin

from .models import Post, PostImage, PostVote, PostShare


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
