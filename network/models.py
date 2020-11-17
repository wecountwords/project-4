from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts_by_author")
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.like_count
        }


class Follower(models.Model):
    # follower is a member (user) who follows a post author.
    # the author will be added on first post
    # the follower and updated relationship will be added when the author is followed
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    author = models.ForeignKey("User", on_delete=models.CASCADE)


class Like(models.Model):
    # a user can like a post or unlike a post.
    post_id = models.PositiveSmallIntegerField()
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="favorite_posts")
    like = models.BooleanField()
