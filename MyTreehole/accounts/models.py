from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    is_muted = models.BooleanField(default=False)  # 禁言状态
    muted_until = models.DateTimeField(null=True, blank=True)  # 禁言截止时间
    mute_reason = models.TextField(blank=True)  # 禁言原因
    created_at = models.DateTimeField(auto_now_add=True)  # 添加创建时间

    def __str__(self):
        return f'{self.user.username} Profile'

    def is_currently_muted(self):
        """检查用户当前是否被禁言"""
        if not self.is_muted:
            return False
        if self.muted_until and self.muted_until < timezone.now():
            # 禁言已过期
            self.is_muted = False
            self.muted_until = None
            self.save()
            return False
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 调整头像大小
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
            except Exception as e:
                print(f"头像处理失败: {e}")


# 导入timezone
from django.utils import timezone


# 改进的信号处理器
@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    处理用户保存信号
    为新用户创建Profile，为现有用户确保有Profile
    """
    if created:
        # 新用户：创建Profile
        Profile.objects.create(user=instance)
    else:
        # 现有用户：确保有Profile
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        else:
            # 如果已有Profile，保存它
            instance.profile.save()