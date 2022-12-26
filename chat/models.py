from django.db import models
from django.contrib.auth import get_user_model

# utils
from utils.helpers import get_uuid

User = get_user_model()


class CommunityChatRoom(models.Model):

    community = models.ForeignKey(
        'community.Community', on_delete=models.CASCADE, related_name='chat_rooms'
    )

    slug = models.SlugField(max_length=255, unique=True, default=get_uuid)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Community Chat Room'
        verbose_name_plural = 'Community Chat Rooms'
        ordering = ['-created_at']


class CommunityChatRoomMember(models.Model):

    chat_room = models.ForeignKey(
        'chat.CommunityChatRoom', on_delete=models.CASCADE, related_name='members'
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_room_memberships'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Community Chat Room Member'
        verbose_name_plural = 'Community Chat Room Members'
        ordering = ['-created_at']


class CommunityChatRoomMessage(models.Model):

    chat_room = models.ForeignKey(
        'chat.CommunityChatRoom', on_delete=models.CASCADE, related_name='messages'
    )

    user = models.ForeignKey(
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
