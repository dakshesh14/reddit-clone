from django.urls import path

from .apis import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # for community posts
    path(
        'community/<slug>/posts/',
        PostListCreateAPIView.as_view(),
        name='post-list-create'
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
