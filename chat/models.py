from django.db import models
from django.contrib.auth import get_user_model

# utils
from utils.helpers import get_uuid

User = get_user_model()


class CommunityChatRoom(models.Model):

    community = models.OneToOneField(
        'community.Community', on_delete=models.CASCADE, related_name='chat_rooms'
    )

    slug = models.SlugField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Community Chat Room'
        verbose_name_plural = 'Community Chat Rooms'
        ordering = ['-created_at']

    def get_online_member_count(self):
        return self.members.filter(is_online=True).count()

    def get_typing_members_username(self):
        return [member.owner.username for member in self.members.filter(is_typing=True)]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_uuid(36)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.community.name} Chat Room"


class CommunityChatRoomMember(models.Model):

    chat_room = models.ForeignKey(
        'chat.CommunityChatRoom', on_delete=models.CASCADE, related_name='members'
    )

    member = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='chat_room_members'
    )

    is_online = models.BooleanField(default=False)
    is_typing = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.username} joined {self.chat_room.community.name} Chat Room"

    class Meta:
        verbose_name = 'Community Chat Room Member'
        verbose_name_plural = 'Community Chat Room Members'
        ordering = ['-created_at']


class CommunityChatRoomMessage(models.Model):

    chat_room = models.ForeignKey(
        'chat.CommunityChatRoom', on_delete=models.CASCADE, related_name='messages'
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_room_messages'
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Community Chat Room Message'
        verbose_name_plural = 'Community Chat Room Messages'
        ordering = ['-created_at']
