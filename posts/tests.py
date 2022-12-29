import random
import datetime

# django
from django.test import TestCase
from django.contrib.auth import get_user_model

# local
from utils.post_rank_helpers import rank_posts
# models
from community.models import Community
from .models import Post, PostVote, Comment, PostShare

User = get_user_model()


class PostTestCase(TestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username='test_user',
            email='test@user.com'
        )

        # create a community
        self.community = Community.objects.create(
            name='Test Community',
            description='Test Description',
            owner=self.user
        )

        # create 10 posts
        for i in range(5):
            Post.objects.create(
                title=f'Test Post {i}',
                content='Test Content',
                owner=self.user,
                community=self.community
            )

        # add random votes, shares and comments to any post
        count = 0
        for post in Post.objects.all():
            count += 1
            for i in range(5):
                # create a random user
                user = User.objects.create_user(
                    username=f'testuser{i}{count}',
                    email=f'testuser{i}{count}@gmail.com'
                )

                # create a random vote
                if random.randint(0, 1) == 0:
                    PostVote.objects.create(
                        post=post,
                        owner=user,
                        upvoted=True
                    )
                elif random.randint(0, 1) == 1:
                    PostVote.objects.create(
                        post=post,
                        owner=user,
                        downvoted=True
                    )

                # create a random share
                if random.randint(0, 1) == 0:
                    PostShare.objects.create(
                        post=post,
                        owner=user
                    )

                # create a random comment
                if random.randint(0, 1) == 0:
                    Comment.objects.create(
                        post=post,
                        owner=user,
                        content='Test Comment'
                    )

    def test_rank_posts(self):
        # get all the posts
        posts = Post.objects.all()

        today_date = datetime.datetime.now().date()
        one_month_after = today_date + datetime.timedelta(days=30)

        # check rank function is working
        rank_posts(posts, today_date, one_month_after)
        rank_posts(posts)
