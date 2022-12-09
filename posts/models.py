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


class JoinedCommunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')
        verbose_name = 'Joined Community'
        verbose_name_plural = 'Joined Communities'

    def __str__(self):
        return f'{self.user} joined {self.community}'


def SET_OLDEST_MEMBER(collector, field, sub_objs, using):
    oldest_members = JoinedCommunity.objects.filter(
        community=sub_objs[0]
    ).order_by('date_joined')
    if oldest_members.exists():
        collector.add_field_update(
            field,
            oldest_members.first().user,
            sub_objs
        )
    else:
        sub_objs[0].delete()


class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=325, unique=True)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=SET_OLDEST_MEMBER,
        related_name='communities',
        null=True,
    )

    members = models.ManyToManyField(User, through=JoinedCommunity)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'community'
        verbose_name_plural = 'communities'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/communities/%s/" % self.slug

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)


class PostImage(models.Model):
    image = ProcessedImageField(
        upload_to='post_images',
        processors=[ResizeToFill(900, 900)],
        format='JPEG',
        options={'quality': 100},
    )
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} image'


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=325, unique=True)

    community = models.ForeignKey(
        Community,
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

    def get_absolute_url(self):
        return "/communities/%s/%s/" % (self.community.slug, self.slug)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title) + '-' + get_uuid()
        super(Post, self).save(*args, **kwargs)
