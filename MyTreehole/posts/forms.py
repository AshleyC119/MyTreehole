from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'privacy']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }