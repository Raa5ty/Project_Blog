# blog_app/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите содержание поста...',
                'rows': 10
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }
    
    def clean_title(self):
        """Валидация заголовка"""
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Заголовок должен содержать минимум 3 символа')
        if len(title) > 200:
            raise forms.ValidationError('Заголовок не может превышать 200 символов')
        return title
    
    def clean_content(self):
        """Валидация содержания"""
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('Содержание должно содержать минимум 10 символов')
        return content
