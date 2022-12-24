from rest_framework import serializers

from posts.models import Post, Community, PostImage, JoinedCommunity

from accounts.api.serializers import UserSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'post',)


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
            'created_at',
            'updated_at',
            'is_member',
            'number_of_members',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at',)
        extra_kwargs = {
            'members': {'required': False},
            'owner': {'required': False},
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


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(
        many=True, read_only=True, source='get_images'
    )
    thumbnail = PostImageSerializer(source='get_thumbnail', read_only=True)

    community_details = serializers.SerializerMethodField()
    owner_details = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'slug',
            'community',
            'community_details',
            'owner',
            'owner_details',
            'images',
            'thumbnail',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at',)
        extra_kwargs = {
            'owner': {'required': False},
        }

    def get_community_details(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = CommunitySerializer(
            obj.community, context=serializer_context
        )
        return serializer.data

    def get_owner_details(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = UserSerializer(
            obj.owner, context=serializer_context
        )
        return serializer.data

    def validate(self, data):
        if len(self.context['request'].FILES.getlist('images')) <= 0:
            raise serializers.ValidationError(
                {'images': 'You must upload at least one image'}
            )
        return data

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image_data in images_data.getlist('images'):
            PostImage.objects.create(post=post, image=image_data)
        return post
