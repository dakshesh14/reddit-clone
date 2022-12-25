from django.urls import path

from .apis import (
    CommunityListCreateAPIView,
    CommunityRetrieveUpdateDestroyAPIView,
    JoinedCommunityListCreateAPIView,
)

urlpatterns = [
    # communities
    path(
        'community/',
        CommunityListCreateAPIView.as_view(),
        name='community-list-create'

    ),
    path(
        'community/<slug:slug>/',
        CommunityRetrieveUpdateDestroyAPIView.as_view(),
        name='community-retrieve-update-destroy'
    ),

    # for joining and leaving communities
    path(
        'my-communities/',
        JoinedCommunityListCreateAPIView.as_view(),
        name='joined-community-list-create'
    ),
]
