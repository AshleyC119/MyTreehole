from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Comment, Like


@login_required
def add_comment(request, post_id):
    from posts.models import Post
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, '评论发布成功！')
        else:
            messages.error(request, '评论内容不能为空！')

    return redirect('post_detail', pk=post_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 检查权限：只有评论作者或帖子作者可以删除评论
    if request.user == comment.author or request.user == comment.post.author:
        post_id = comment.post.id
        comment.delete()
        messages.success(request, '评论已删除')
        return redirect('post_detail', pk=post_id)
    else:
        messages.error(request, '你没有权限删除此评论')
        return redirect('post_detail', pk=comment.post.id)


@login_required
def toggle_like(request, post_id):
    from posts.models import Post
    post = get_object_or_404(Post, id=post_id)

    # 检查用户是否已经点赞
    like_exists = Like.objects.filter(post=post, user=request.user).exists()

    if like_exists:
        # 如果已点赞，则取消点赞
        Like.objects.filter(post=post, user=request.user).delete()
        messages.info(request, '已取消点赞')
    else:
        # 如果未点赞，则添加点赞
        Like.objects.create(post=post, user=request.user)
        messages.success(request, '点赞成功！')

    return redirect('post_detail', pk=post_id)