from rest_framework import serializers
# local
from chat.models import CommunityChatRoom, CommunityChatRoomMember, CommunityChatRoomMessage

from accounts.api.serializers import UserSerializer


class CommunityChatRoomSerializer(serializers.ModelSerializer):
    online_member_count = serializers.IntegerField(
        read_only=True, source='get_online_member_count'
    )
    typing_members_username = serializers.ListField(
        read_only=True, source='get_typing_members_username'
    )

    class Meta:
        model = CommunityChatRoom
        extra_kwargs = {
            'slug': {'required': False},
        }
        fields = (
            'id',
            'community',
            'slug',
            'created_at',
            'updated_at',
            'online_member_count',
            'typing_members_username',
        )

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CommunityChatRoom.objects.all(),
                fields=['community'],
            ),
        ]


class CommunityChatRoomMemberSerializer(serializers.ModelSerializer):
    member_detail = UserSerializer(read_only=True, source='member')

    class Meta:
        model = CommunityChatRoomMember
        fields = (
            'id',
            'chat_room',
            'member',
            'member_detail',
            'is_online',
            'is_typing',
            'created_at',
            'updated_at',
        )


class CommunityChatRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityChatRoomMessage
        fields = '__all__'
