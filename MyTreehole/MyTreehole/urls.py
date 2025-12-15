from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView

# 创建一个CSRF豁免的登录视图
csrf_exempt_login_view = csrf_exempt(LoginView.as_view(template_name='accounts/login.html'))

urlpatterns = [
    path('', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('interactions/', include('interactions.urls')),
    path('admin/', admin.site.urls),

    # 添加一个专门的登录路径（CSRF豁免）
    path('login-no-csrf/', csrf_exempt_login_view, name='login_no_csrf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)