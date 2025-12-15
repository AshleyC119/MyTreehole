from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '帖子发布成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


def post_list(request):
    posts_list = Post.objects.filter(privacy='public')
    paginator = Paginator(posts_list, 10)  # 每页10个帖子

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '你没有权限编辑此帖子！')
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '帖子更新成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '你没有权限删除此帖子！')
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '帖子删除成功！')
        return redirect('post_list')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})