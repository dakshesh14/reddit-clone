from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.files import File as DjangoFile

# imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# utils
from utils.helpers import get_random_identicon

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
    if oldest_members.exists() and oldest_members.first().user != sub_objs[0].owner:
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

    logo = models.ImageField(
        upload_to='community_logos',
    )
    processed_logo = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 60},
    )
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=SET_OLDEST_MEMBER,
        related_name='owned_communities',
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
        import requests
        from django.core.files.temp import NamedTemporaryFile

        if not self.id:
            self.slug = slugify(self.name)

            if not self.logo:
                response = requests.get(get_random_identicon(self.name))
                img_temp = NamedTemporaryFile()
                img_temp.write(response.content)
                img_temp.flush()
                self.logo.save(
                    f'{self.slug}.jpg',
                    DjangoFile(img_temp),
                    save=False
                )

        self.name = self.name.lower()
        super(Community, self).save(*args, **kwargs)
