from django.shortcuts import get_object_or_404
# rest framework
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# serializers
from .serializers import CommunitySerializer, JoinedCommunitySerializer
# models
from community.models import Community, JoinedCommunity
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
