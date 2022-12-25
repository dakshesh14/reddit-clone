from rest_framework import serializers

from community.models import Community, JoinedCommunity


class CommunitySerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()
    number_of_members = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = (
            'id',
            'name',
            'slug',
            'owner',
            'description',
            'logo',
            'created_at',
            'updated_at',
            'is_member',
            'number_of_members',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at',)
        extra_kwargs = {
            'members': {'required': False},
            'owner': {'required': False},
            'logo': {'required': False},
        }

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return JoinedCommunity.objects.filter(
                community=obj,
                user=request.user,
            ).exists()
        return False

    def get_number_of_members(self, obj):
        return obj.members.count()


class JoinedCommunitySerializer(serializers.ModelSerializer):
    community_details = CommunitySerializer(
        source='community', read_only=True,
    )
    communities = serializers.SlugRelatedField(
        queryset=Community.objects.all(),
        many=True,
        write_only=True,
        slug_field='slug',
    )

    class Meta:
        model = JoinedCommunity
        fields = ('id', 'community_details', 'communities',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'community': {'required': False},
        }

    def get_community_details(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = CommunitySerializer(
            obj.community, context=serializer_context
        )
        return serializer.data
