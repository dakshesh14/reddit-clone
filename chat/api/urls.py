from django.urls import path

from .apis import (
    ChatRoomCreateAPIView,
    ChatRoomRetrieveDestroyAPIView,
    ChatRoomMemberList,
    JoinLeaveChatRoomAPIView
)

urlpatterns = [
    path(
        'create-room/',
        ChatRoomCreateAPIView.as_view(),
        name='create'
    ),
    # room detail
    path(
        'room/<slug:slug>/',
        ChatRoomRetrieveDestroyAPIView.as_view(),
        name='retrieve-destroy'
    ),

    # room members
    path(
        'room/<slug:slug>/members/',
        ChatRoomMemberList.as_view(),
        name='members'
    ),

    # join leave room
    path(
        'room/<slug:slug>/join-leave/',
        JoinLeaveChatRoomAPIView.as_view(),
        name='join-leave'
    ),

]
