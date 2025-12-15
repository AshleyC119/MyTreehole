"""
修复interactions导入问题的脚本
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyTreehole.settings')
django.setup()


def check_interactions():
    """检查interactions应用"""
    from django.apps import apps

    # 检查interactions是否已注册
    installed_apps = [app.name for app in apps.get_app_configs()]
    print("已安装的应用:", installed_apps)

    if 'interactions' in installed_apps:
        print("✓ interactions应用已注册")

        # 尝试导入模型
        try:
            from interactions.models import Comment, Like
            print("✓ interactions模型导入成功")

            # 检查是否有数据
            comment_count = Comment.objects.count()
            like_count = Like.objects.count()
            print(f"  评论数: {comment_count}, 点赞数: {like_count}")

            return True
        except Exception as e:
            print(f"✗ interactions模型导入失败: {e}")
            return False
    else:
        print("✗ interactions应用未注册")
        return False


def create_interactions_app():
    """如果interactions应用不存在，创建它"""
    # 检查interactions目录是否存在
    interactions_dir = os.path.join(os.path.dirname(__file__), 'interactions')
    if not os.path.exists(interactions_dir):
        print("创建interactions目录...")
        os.makedirs(interactions_dir)

        # 创建必要的文件
        files_to_create = [
            ('__init__.py', ''),
            ('apps.py', """from django.apps import AppConfig

class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interactions'

    def ready(self):
        import interactions.signals
"""),
            ('models.py', """from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
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
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f'{self.user} 喜欢 {self.post}'
"""),
            ('admin.py', """from django.contrib import admin
from .models import Comment, Like

admin.site.register(Comment)
admin.site.register(Like)
"""),
            ('views.py', """from django.shortcuts import render
# 暂时留空
"""),
            ('urls.py', """from django.urls import path
from . import views

urlpatterns = [
    # URL配置
]
"""),
            ('signals.py', """# 信号处理器
"""),
        ]

        for filename, content in files_to_create:
            filepath = os.path.join(interactions_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"创建 {filename}")

    print("✓ interactions应用文件已创建")


if __name__ == '__main__':
    print("=" * 50)
    print("检查interactions应用状态")
    print("=" * 50)

    if not check_interactions():
        print("\n尝试修复...")
        create_interactions_app()
        print("\n修复完成，请重新运行迁移命令")
        print("python manage.py makemigrations interactions")
        print("python manage.py migrate")
    else:
        print("\n✓ interactions应用状态正常")