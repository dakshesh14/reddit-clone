from rest_framework import serializers

from posts.models import Post, PostImage, Comment, PostShare

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

    votes = serializers.IntegerField(
        read_only=True, source='get_votes'
    )

    upvoted = serializers.SerializerMethodField()
    downvoted = serializers.SerializerMethodField()

    comment_count = serializers.IntegerField(
        read_only=True, source='get_comment_count'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'slug',
            'votes',
            'upvoted',
            'downvoted',
            'comment_count',
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

    def get_upvoted(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.votes.filter(owner=user, upvoted=True).exists():
                return True
        return False

    def get_downvoted(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.votes.filter(owner=user, downvoted=True).exists():
                return True
        return False

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


class CommentSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField()
    votes = serializers.IntegerField(
        read_only=True, source='get_votes'
    )

    upvoted = serializers.SerializerMethodField()
    downvoted = serializers.SerializerMethodField()

    replies = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField(
        read_only=True, source='get_reply_count'
    )

    can_reply = serializers.BooleanField(
        read_only=True, source='get_can_reply'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'post',
            'parent',
            'votes',
            'can_reply',
            'upvoted',
            'downvoted',
            'replies',
            'reply_count',
            'owner',
            'owner_details',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at',)
        extra_kwargs = {
            'owner': {'required': False},
            'post': {'required': False},
        }

    def get_replies(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = CommentSerializer(
            obj.replies.all(), context=serializer_context, many=True
        )
        return serializer.data

    def get_upvoted(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.votes.filter(owner=user, upvoted=True).exists():
                return True
        return False

    def get_downvoted(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.votes.filter(owner=user, downvoted=True).exists():
                return True
        return False

    def get_owner_details(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = UserSerializer(
            obj.owner, context=serializer_context
        )
        return serializer.data

    def validate(self, data):
        # check for comment depth
        if self.context['request'].data.get('parent'):
            parent = Comment.objects.get(
                id=self.context['request'].data.get('parent')
            )
            if parent.get_comment_depth() >= 3:
                raise serializers.ValidationError(
                    {'parent': 'Comment depth exceeded.'}
                )

        if self.context['request'].user.is_authenticated:
            data['owner'] = self.context['request'].user

        return data


class PostShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostShare
        fields = ('id', 'post', 'owner', 'created_at',)
        read_only_fields = ('id', 'created_at', 'owner', 'post')
        extra_kwargs = {
            'owner': {'required': False},
        }
