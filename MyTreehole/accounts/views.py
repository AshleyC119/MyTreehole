from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, MuteUserForm, AdminSearchForm
from .models import Profile
from posts.models import Post
from interactions.models import Comment


# 管理员装饰器
def admin_required(view_func):
    """检查用户是否为管理员的装饰器"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, '请先登录！')
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(request, '您没有管理员权限！')
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@admin_required
def admin_dashboard(request):
    """管理员仪表板"""
    # 基本统计
    stats = {
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'muted_users': Profile.objects.filter(is_muted=True).count(),
        'active_today': User.objects.filter(last_login__date=timezone.now().date()).count(),
    }

    # 最近注册的用户
    recent_users = User.objects.order_by('-date_joined')[:10]

    # 最近帖子
    recent_posts = Post.objects.order_by('-created_at')[:10]

    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_posts': recent_posts,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@admin_required
def admin_users(request):
    """用户管理页面"""
    users = User.objects.all().order_by('-date_joined')

    # 搜索功能
    search_form = AdminSearchForm(request.GET or None)
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__bio__icontains=query)
        )

    # 分页
    from django.core.paginator import Paginator
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_form': search_form,
    }

    return render(request, 'accounts/admin_users.html', context)


@login_required
@admin_required
def admin_posts(request):
    """帖子管理页面"""
    posts = Post.objects.all().order_by('-created_at')

    # 搜索功能
    search_form = AdminSearchForm(request.GET or None)
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    # 分页
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'search_form': search_form,
    }

    return render(request, 'accounts/admin_posts.html', context)


@login_required
@admin_required
def toggle_user_mute(request, user_id):
    """禁言/解除禁言用户"""
    target_user = get_object_or_404(User, id=user_id)
    profile = target_user.profile

    if request.method == 'POST':
        form = MuteUserForm(request.POST)
        if form.is_valid():
            duration_choice = form.cleaned_data['duration']
            reason = form.cleaned_data['reason']

            if profile.is_muted:
                # 解除禁言
                profile.is_muted = False
                profile.muted_until = None
                profile.mute_reason = ''
                profile.save()

                # 记录操作日志
                from django.contrib.admin.models import LogEntry, CHANGE
                from django.contrib.contenttypes.models import ContentType

                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(Profile).pk,
                    object_id=profile.id,
                    object_repr=str(profile),
                    action_flag=CHANGE,
                    change_message=f'解除禁言，操作者：{request.user.username}'
                )

                messages.success(request, f'已解除用户 {target_user.username} 的禁言')
            else:
                # 禁言用户
                profile.is_muted = True
                profile.mute_reason = reason

                # 设置禁言截止时间
                hours = int(duration_choice)
                if hours == 0:
                    profile.muted_until = None  # 永久禁言
                else:
                    profile.muted_until = timezone.now() + timedelta(hours=hours)

                profile.save()

                messages.success(request, f'已禁言用户 {target_user.username}')

            return redirect('admin_users')
    else:
        # 如果是GET请求，显示禁言表单
        form = MuteUserForm()
        context = {
            'target_user': target_user,
            'form': form,
            'is_muted': profile.is_muted,
        }
        return render(request, 'accounts/toggle_mute.html', context)


@login_required
@admin_required
def admin_delete_post(request, post_id):
    """管理员删除任意帖子"""
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # 记录删除前的内容（用于日志）
        post_title = post.title
        post_author = post.author.username

        # 删除帖子
        post.delete()

        # 发送通知给帖子作者（可选）
        messages.success(request, f'已删除帖子 "{post_title}" (作者: {post_author})')

        # 重定向到帖子列表或管理页面
        if 'from_admin' in request.GET:
            return redirect('admin_posts')
        return redirect('post_list')

    # 显示确认页面
    context = {
        'post': post,
        'from_admin': request.GET.get('from_admin', False),
    }
    return render(request, 'accounts/admin_confirm_delete_post.html', context)


@login_required
@admin_required
def admin_delete_comment(request, comment_id):
    """管理员删除任意评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        # 记录删除前的内容
        comment_content = comment.content[:50] + '...' if len(comment.content) > 50 else comment.content
        comment_author = comment.author.username

        # 删除评论
        comment.delete()

        messages.success(request, f'已删除评论 "{comment_content}" (作者: {comment_author})')

        # 重定向回原帖子
        return redirect('post_detail', pk=comment.post.id)

    # 显示确认页面
    context = {
        'comment': comment,
    }
    return render(request, 'accounts/admin_confirm_delete_comment.html', context)


# 现有的视图函数...
def home(request):
    # 导入需要的模型
    try:
        from posts.models import Post
        from interactions.models import Comment, Like
    except ImportError as e:
        # 如果导入失败，返回0值
        print(f"导入错误: {e}")
        context = {
            'total_users': User.objects.count(),
            'total_posts': 0,
            'total_comments': 0,
            'total_likes': 0,
        }
    else:
        # 计算社区统计数据
        context = {
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
            'total_comments': Comment.objects.count(),
            'total_likes': Like.objects.count(),
        }

    return render(request, 'accounts/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号 {username} 创建成功！请登录。')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):

    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    try:
        from posts.models import Post
        from interactions.models import Comment, Like
    except ImportError as e:
        # 如果导入失败，设置默认值并打印错误信息
        print(f"导入错误: {e}")
        user_stats = {
            'post_count': 0,
            'comment_count': 0,
            'like_count': 0,
        }
    else:
        user_stats = {
            'post_count': Post.objects.filter(author=request.user).count(),
            'comment_count': Comment.objects.filter(author=request.user).count(),
            'like_count': Like.objects.filter(user=request.user).count(),
        }

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '个人资料已更新！')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_stats': user_stats,
    }
    return render(request, 'accounts/profile.html', context)
