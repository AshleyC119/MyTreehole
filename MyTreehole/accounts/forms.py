from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Profile


# 禁言用户表单
class MuteUserForm(forms.Form):
    DURATION_CHOICES = [
        ('1', '1小时'),
        ('24', '24小时'),
        ('168', '7天'),
        ('720', '30天'),
        ('0', '永久'),
    ]

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        label='禁言时长',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        label='禁言原因',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )

    def get_duration_delta(self, duration_choice):
        """将选择转换为timedelta"""
        hours = int(duration_choice)
        if hours == 0:
            return None  # 永久禁言
        return timedelta(hours=hours)


# 管理员搜索表单
class AdminSearchForm(forms.Form):
    search_type = forms.ChoiceField(
        choices=[
            ('user', '用户'),
            ('post', '帖子'),
            ('comment', '评论'),
        ],
        label='搜索类型',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    query = forms.CharField(
        label='搜索内容',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '输入用户名、帖子标题或关键词...'
        })
    )


# 自定义登录表单
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="用户名或邮箱",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )

    error_messages = {
        'invalid_login': "用户名或密码不正确，请重试。",
        'inactive': "该账户已被禁用，请联系管理员。",
    }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("该邮箱已被注册，请使用其他邮箱。")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'avatar']