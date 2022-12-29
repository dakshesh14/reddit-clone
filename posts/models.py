# utils
from utils.helpers import get_uuid
# django
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

User = get_user_model()


class PostImage(models.Model):
    image = ProcessedImageField(
        upload_to='post_images',
        processors=[ResizeToFill(900, 900)],
        format='JPEG',
        options={'quality': 100},
    )
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.post} image'


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=325, unique=True)

    community = models.ForeignKey(
        'community.Community',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __unicode__(self):
        return self.title

    def get_comment_count(self):
        return self.comments.count()

    def get_comments(self):
        return self.comments.filter(parent=None)

    def get_votes(self):
        return self.votes.filter(upvoted=True).count() - self.votes.filter(downvoted=True).count()

    def get_thumbnail(self):
        return self.images.first()

    def get_images(self):
        return self.images.all()

    def get_absolute_url(self):
        return "/communities/%s/%s/" % (self.community.slug, self.slug)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title) + '-' + get_uuid()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_reply_count(self):
        return self.replies.count()

    def get_comment_depth(self):
        if self.parent is None:
            return 0
        return self.parent.get_comment_depth() + 1

    def get_can_reply(self):
        return self.get_comment_depth() < 5

    def get_replies(self):
        return self.replies.all()

    def get_votes(self):
        return self.votes.filter(upvoted=True).count() - self.votes.filter(downvoted=True).count()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self) -> str:
        return self.content

    def save(self, *args, **kwargs):
        if self.get_can_reply():
            super(Comment, self).save(*args, **kwargs)
        else:
            raise ValueError('Maximum comment depth reached.')


class VotingBaseModel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_owner',
    )

    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.owner} voted {self.post}'

    def save(self, *args, **kwargs):
        if self.upvoted and self.downvoted:
            raise ValueError('Cannot upvote and downvote at the same time')
        super(VotingBaseModel, self).save(*args, **kwargs)


class PostVote(VotingBaseModel):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='votes'
    )

    class Meta:
        unique_together = ('owner', 'post')

    def __str__(self):
        return f'{self.owner} voted {self.post}'


class CommentVote(VotingBaseModel):
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='votes'
    )

    class Meta:
        unique_together = ('owner', 'comment')

    def __str__(self):
        return f'{self.owner} voted {self.comment}'


class PostShare(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='shares'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_shares',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'post')

    def __str__(self):
        return f'{self.owner} shared {self.post}'

    def save(self, *args, **kwargs):
        super(PostShare, self).save(*args, **kwargs)
