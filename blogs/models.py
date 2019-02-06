from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=30, unique=True)
    post_content = models.CharField(max_length=2500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title

    class Meta:
        ordering = ('post_title',)


class BlogUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=9, unique=True, default="")
    liked_posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        ordering = ('user__last_name',)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return str(self.comment_id)

