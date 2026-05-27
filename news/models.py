from django.db import models
from django.conf import settings
from .resource import POST_TYPES, paper, news
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = (Post.objects.filter(author = self).aggregate(total = Sum('rating'))['total'])*3
        author_comment_rating = Comment.objects.filter(user = self.user).aggregate(total=Sum('rating'))['total']
        posts_comment_rating = Comment.objects.filter(post__author=self).aggregate(total=Sum('rating'))['total']
        self.rating = posts_comment_rating + author_comment_rating + posts_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=paper)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        else:
            return self.text

    def __str__(self):
        return f'{self.title}: {self.text}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    time_im = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()