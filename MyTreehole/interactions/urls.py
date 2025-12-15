from django.urls import path
from . import views

urlpatterns = [
    # 评论相关
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # 点赞相关
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]