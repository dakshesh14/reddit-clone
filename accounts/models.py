from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# utils
from utils.helpers import get_random_avatar


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        if not extra_fields.get('avatar', None):
            image_url = get_random_avatar(extra_fields.get('username', email))

            import requests
            from django.core.files.base import ContentFile
            response = requests.get(image_url)
            extra_fields['avatar'] = ContentFile(
                response.content, name=f'{extra_fields.get("username",email)}.jpg'
            )

        user = self.model(email=self.normalize_email(
            email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_onboarded = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    is_admin = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    avatar = models.ImageField(
        upload_to='avatars',
    )
    processed_avatar = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 60},
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
