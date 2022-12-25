from rest_framework import serializers

from posts.models import Post, PostImage

from accounts.api.serializers import UserSerializer

from community.api.serializers import CommunitySerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'post',)


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
