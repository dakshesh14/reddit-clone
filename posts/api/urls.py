from django.urls import path

from .apis import (
    CommunityListCreateAPIView,
    CommunityRetrieveUpdateDestroyAPIView,
    JoinedCommunityListCreateAPIView,
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # communities
    path(
        'communities/',
        CommunityListCreateAPIView.as_view(),
        name='community-list-create'

    ),
    path(
        'communities/<slug:slug>/',
        CommunityRetrieveUpdateDestroyAPIView.as_view(),
        name='community-retrieve-update-destroy'
    ),

    # for community posts
    path(
        'community/<slug>/posts/',
        PostListCreateAPIView.as_view(),
        name='post-list-create'
    ),

    # for joining and leaving communities
    path(
        'my-communities/',
        JoinedCommunityListCreateAPIView.as_view(),
        name='joined-community-list-create'
    ),

    # for posts
    path(
        'posts/',
        PostListCreateAPIView.as_view(),
        name='post-list-create',
    ),
    path(
        'posts/my-posts/',
        PostListCreateAPIView.as_view(),
        name='post-list-create'
    ),
    path(
        'posts/my-feed/',
        PostListCreateAPIView.as_view(),
        name='post-list-create'
    ),
    path(
        'posts/<slug:slug>/',
        PostRetrieveUpdateDestroyAPIView.as_view(),
        name='post-retrieve-update-destroy'
    ),
]
