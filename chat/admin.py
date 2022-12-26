from django.contrib import admin

# Register your models here.
from .models import CommunityChatRoom, CommunityChatRoomMember, CommunityChatRoomMessage


@admin.register(CommunityChatRoom)
class CommunityChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityChatRoomMember)
class CommunityChatRoomMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityChatRoomMessage)
class CommunityChatRoomMessageAdmin(admin.ModelAdmin):
    pass
