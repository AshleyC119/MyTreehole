from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home, register, profile, admin_dashboard, admin_users, admin_posts, toggle_user_mute, \
    admin_delete_post, admin_delete_comment

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),

    # 管理员URL前缀为 admin_panel/
    path('admin_panel/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_panel/users/', admin_users, name='admin_users'),
    path('admin_panel/posts/', admin_posts, name='admin_posts'),
    path('admin_panel/user/<int:user_id>/toggle-mute/', toggle_user_mute, name='toggle_user_mute'),
    path('admin_panel/post/<int:post_id>/delete/', admin_delete_post, name='admin_delete_post'),
    path('admin_panel/comment/<int:comment_id>/delete/', admin_delete_comment, name='admin_delete_comment'),
]