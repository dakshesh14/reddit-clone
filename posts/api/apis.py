from django.shortcuts import get_object_or_404
# rest framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# serializers
from .serializers import PostSerializer
# models
from posts.models import Post
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
