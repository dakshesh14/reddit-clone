from django.shortcuts import get_object_or_404
# rest framework
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# serializers
from .serializers import PostSerializer, CommentSerializer
# models
from posts.models import Post, PostVote, Comment, CommentVote
from community.models import Community
# utils
from utils.permissions import (IsOwnerOrReadonly,)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        community_slug = self.kwargs.get('slug')
        if community_slug:
            return Post.objects.filter(community__slug=community_slug).all()
        else:
            my_posts = self.request.query_params.get('my-posts')
            my_feed = self.request.query_params.get('my-feed')

            if my_posts:
                return Post.objects.filter(owner=self.request.user).all()
            elif my_feed:
                return Post.objects.filter(community__joinedcommunity__user=self.request.user).all()
            else:
                return Post.objects.all()

    def perform_create(self, serializer):
        community_slug = self.kwargs.get('slug')
        community = get_object_or_404(Community, slug=community_slug)

        serializer.save(owner=self.request.user, community=community)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    lookup_field = 'slug'

    permission_classes = [IsOwnerOrReadonly, ]


class PostVoteAPIView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    lookup_field = 'slug'

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        upvoted = request.data.get('upvote', True)
        downvoted = request.data.get('downvote', False)

        if upvoted == downvoted:
            return Response({'error': 'You can only upvote or downvote.'}, status=400)

        vote, created = PostVote.objects.get_or_create(
            owner=request.user,
            post=post,
            upvoted=upvoted,
            downvoted=downvoted,
        )

        if not created:
            vote.delete()
        else:
            vote.upvoted = upvoted
            vote.downvoted = downvoted
            vote.save()

        return Response(self.get_serializer(post).data)


class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Comment.objects.filter(post__slug=post_slug, parent=None).all()

    def perform_create(self, serializer):
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug)

        serializer.save(owner=self.request.user, post=post)


class PostCommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    lookup_field = 'pk'

    permission_classes = [IsOwnerOrReadonly, ]


class PostCommentVoteAPIView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    lookup_field = 'pk'

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        comment = self.get_object()

        upvoted = request.data.get('upvote', True)
        downvoted = request.data.get('downvote', False)

        if upvoted == downvoted:
            return Response({'error': 'You can only upvote or downvote.'}, status=400)

        vote, created = CommentVote.objects.get_or_create(
            owner=request.user,
            comment=comment,
        )

        if not created:
            vote.delete()
        else:
            if vote.upvoted == upvoted and vote.downvoted == downvoted:
                return Response({'error': 'You can only upvote or downvote.'}, status=400)

            vote.upvoted = upvoted
            vote.downvoted = downvoted
            vote.save()

        return Response(self.get_serializer(comment).data)
