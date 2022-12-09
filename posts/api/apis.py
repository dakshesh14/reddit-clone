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
        serializer = JoinedCommunitySerializer(data=request.data)
        if serializer.is_valid():
            community = Community.objects.get(
                slug=serializer.validated_data['community'].slug
            )
            if JoinedCommunity.objects.filter(user=request.user, community=community).exists():
                return Response({'detail': 'You have already joined this community.'}, status=400)

            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def delete(self, request, _=None):
        serializer = JoinedCommunitySerializer(data=request.data)
        if serializer.is_valid():
            community = Community.objects.get(
                slug=serializer.validated_data['community'].slug
            )
            if not JoinedCommunity.objects.filter(user=request.user, community=community).exists():
                return Response({'detail': 'You have not joined this community.'}, status=400)

            JoinedCommunity.objects.filter(
                user=request.user, community=community).delete()
            return Response(status=204)

        return Response(serializer.errors, status=400)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    lookup_field = 'slug'

    permission_classes = [IsOwnerOrReadonly, ]
