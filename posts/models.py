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


class VotingBaseModel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_votes',
    )

    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        unique_together = ('owner', 'post')

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

    def __str__(self):
        return f'{self.owner} voted {self.post}'
