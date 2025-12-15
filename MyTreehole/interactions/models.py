from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    # 使用字符串引用，避免循环导入
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'评论 by {self.author}'


class Like(models.Model):
    # 使用字符串引用，避免循环导入
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']  # 防止重复点赞

    def __str__(self):
        return f'{self.user} 喜欢 {self.post}'