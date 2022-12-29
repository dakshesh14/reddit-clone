from django.shortcuts import get_object_or_404
# rest framework
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# serializers
from .serializers import PostSerializer, CommentSerializer, PostShareSerializer
# models
from posts.models import Post, PostVote, Comment, CommentVote, PostShare
from community.models import Community
# utils
from utils.permissions import (IsOwnerOrReadonly,)
from utils.post_rank_helpers import rank_posts


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        community_slug = self.kwargs.get('slug')
        if community_slug:
            return rank_posts(Post.objects.filter(community__slug=community_slug).all())
        else:

            url = self.request.build_absolute_uri()

            my_posts = 'my-posts' in url
            my_feed = 'my-feed' in url

            filter_by = self.request.query_params.get('filter_by', None)

            start_date = None
            end_date = None

            if filter_by == "hot":

                from datetime import timedelta, timezone

                start_date = timezone.now() - timedelta(days=1)
                end_date = timezone.now()

            elif filter_by == "week":
                from datetime import timedelta, timezone

                start_date = timezone.now() - timedelta(days=7)
                end_date = timezone.now()

            elif filter_by == "month":
                from datetime import timedelta, timezone

                start_date = timezone.now() - timedelta(days=30)
                end_date = timezone.now()

            elif filter_by == "year":
                from datetime import timedelta, timezone

                start_date = timezone.now() - timedelta(days=365)
                end_date = timezone.now()

            posts = Post.objects.none()

            if my_posts:
                posts = Post.objects.filter(owner=self.request.user).all()
            elif my_feed:
                posts = Post.objects.filter(
                    community__joinedcommunity__user=self.request.user).all()
            else:
                posts = Post.objects.all()

            return rank_posts(posts, start_date=start_date, end_date=end_date)

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


class PostShareAPIView(generics.GenericAPIView):
    queryset = PostShare.objects.all()
    serializer_class = PostShareSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug)

        if PostShare.objects.filter(owner=self.request.user, post=post).exists():
            return Response({'error': 'You have already shared this post.'}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user, post=post)

        return Response(serializer.data)
