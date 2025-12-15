from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建Profile"""
    if created:
        # 检查是否已存在Profile，避免重复创建
        try:
            instance.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """用户保存时确保有Profile"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # 如果用户没有Profile，创建一个
        Profile.objects.get_or_create(user=instance)