from django.shortcuts import get_object_or_404
# rest framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# serializers
from .serializers import (
    CommunityChatRoomMemberSerializer,
    CommunityChatRoomMessageSerializer,
    CommunityChatRoomSerializer
)
# models
from community.models import Community
from chat.models import (
    CommunityChatRoom,
    CommunityChatRoomMember,
    CommunityChatRoomMessage
)
# utils
from utils.permissions import (IsCommunityOwnerOrReadonly,)


class ChatRoomCreateAPIView(generics.CreateAPIView):
    serializer_class = CommunityChatRoomSerializer
    permission_classes = [IsCommunityOwnerOrReadonly, ]


class ChatRoomRetrieveDestroyAPIView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = CommunityChatRoom.objects.all()
    serializer_class = CommunityChatRoomSerializer
    permission_classes = [IsCommunityOwnerOrReadonly, ]

    lookup_field = 'slug'


class ChatRoomMemberList(generics.ListAPIView):
    serializer_class = CommunityChatRoomMemberSerializer
    permission_classes = [IsCommunityOwnerOrReadonly, ]

    def get_queryset(self):
        room_slug = self.kwargs.get('slug')
        return CommunityChatRoomMember.objects.filter(chat_room__slug=room_slug)


class JoinLeaveChatRoomAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, slug=None):
        room = get_object_or_404(CommunityChatRoom, slug=slug)
        if CommunityChatRoomMember.objects.filter(member=request.user, chat_room=room).exists():
            return Response({'detail': 'You are already a member of this community.'}, status=400)
        else:
            CommunityChatRoomMember.objects.create(
                member=request.user, chat_room=room
            )
            return Response({
                'detail': 'You have successfully joined this community.',
            }, status=200)

    def delete(self, request, slug=None):
        room = get_object_or_404(CommunityChatRoom, slug=slug)
        if CommunityChatRoomMember.objects.filter(member=request.user, chat_room=room).exists():
            CommunityChatRoomMember.objects.filter(
                member=request.user, chat_room=room
            ).delete()

            return Response({
                'detail': 'You have successfully left this community.',
            }, status=200)
        else:
            return Response({'detail': 'You are not a member of this community.'}, status=400)
