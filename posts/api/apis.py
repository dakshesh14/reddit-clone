from django.shortcuts import get_object_or_404
# rest framework
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# serializers
from .serializers import CommunitySerializer, JoinedCommunitySerializer, PostSerializer, PostImageSerializer
# models
from posts.models import Community, JoinedCommunity, Post, PostImage
# utils
from utils.permissions import (IsOwnerOrReadonly,)


class CommunityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        obj = serializer.save(owner=self.request.user)
        JoinedCommunity.objects.create(user=self.request.user, community=obj)


class CommunityRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    lookup_field = 'slug'

    permission_classes = [IsOwnerOrReadonly, ]


class JoinedCommunityListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, _=None):
        communities = JoinedCommunity.objects.filter(user=request.user)
        serializer = JoinedCommunitySerializer(communities, many=True)
        return Response(serializer.data)

    def post(self, request, _=None):
        communities = request.data.get('communities')
        if communities:
            for community in communities:
                community = get_object_or_404(Community, slug=community)
                if JoinedCommunity.objects.filter(user=request.user, community=community).exists():
                    continue
                # TODO: switch to bulk_create
                JoinedCommunity.objects.create(
                    user=request.user, community=community
                )

            return Response(status=201)
        else:
            return Response({'detail': 'No communities found.'}, status=400)

    def delete(self, request, _=None):
        communities = request.data.get('communities')
        if communities:
            for community in communities:
                community = get_object_or_404(Community, slug=community)
                if not JoinedCommunity.objects.filter(user=request.user, community=community).exists():
                    continue

                JoinedCommunity.objects.filter(
                    user=request.user, community=community
                ).delete()

            return Response(status=204)
        else:
            return Response({'detail': 'No communities found.'}, status=400)


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
