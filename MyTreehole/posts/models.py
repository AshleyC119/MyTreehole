from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    PRIVACY_CHOICES = [
        ('public', '公开'),
        ('friends', '仅好友'),
        ('private', '仅自己'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})