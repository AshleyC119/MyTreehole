from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone


class MuteCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 如果用户已登录且被禁言
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            profile = request.user.profile

            # 检查是否被禁言
            if profile.is_muted:
                # 检查禁言是否已过期
                if profile.muted_until and profile.muted_until < timezone.now():
                    # 禁言已过期，解除禁言
                    profile.is_muted = False
                    profile.muted_until = None
                    profile.save()
                else:
                    # 用户仍被禁言，检查是否试图发布内容
                    restricted_paths = ['/posts/create/', '/interactions/comment/']
                    current_path = request.path

                    for restricted_path in restricted_paths:
                        if restricted_path in current_path and request.method == 'POST':
                            messages.error(request, '您已被禁言，无法发布内容。')
                            return redirect('home')

        response = self.get_response(request)
        return response