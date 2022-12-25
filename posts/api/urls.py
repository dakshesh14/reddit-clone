from django.urls import path

from .apis import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    PostVoteAPIView,
    PostCommentListCreateAPIView,
    PostCommentRetrieveUpdateDestroyAPIView,
    PostCommentVoteAPIView,
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

    # for post votes
    path(
        'posts/<slug:slug>/vote/',
        PostVoteAPIView.as_view(),
        name='post-vote'
    ),

    # for post comments
    path(
        'posts/<slug:slug>/comments/',
        PostCommentListCreateAPIView.as_view(),
        name='post-comment-list-create'
    ),
    path(
        'posts/<slug:slug>/comments/<int:pk>/',
        PostCommentRetrieveUpdateDestroyAPIView.as_view(),
        name='post-comment-retrieve-update-destroy'
    ),

    # for post comment votes
    path(
        'posts/<slug:slug>/comments/<int:pk>/vote/',
        PostCommentVoteAPIView.as_view(),
        name='post-comment-vote'
    ),
]
