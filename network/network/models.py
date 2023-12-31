from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_post = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}: {self.content}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self):
        return f"{self.user} follows {self.following}"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} likes {self.post}"
