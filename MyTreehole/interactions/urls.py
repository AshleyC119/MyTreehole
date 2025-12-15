from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # 两个登录路径：正常和免CSRF
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    # 管理员路径
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/users/', views.admin_users, name='admin_users'),
    path('manage/posts/', views.admin_posts, name='admin_posts'),
    path('manage/user/<int:user_id>/toggle-mute/', views.toggle_user_mute, name='toggle_user_mute'),
    path('manage/post/<int:post_id>/delete/', views.admin_delete_post, name='admin_delete_post'),
    path('manage/comment/<int:comment_id>/delete/', views.admin_delete_comment, name='admin_delete_comment'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]