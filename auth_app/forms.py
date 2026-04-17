# auth_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class RegistrationForm(forms.ModelForm):
    """
    Форма регистрации нового пользователя
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        label='Подтверждение пароля'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
        }
    
    # Валидация email на уникальность
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
    
    # Валидация совпадения паролей
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя или email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    
    class Meta:
        fields = ['username', 'password']


class MessageForm(forms.Form):
    """
    Форма отправки сообщения (для связи)
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        }),
        label='Имя'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш email'
        }),
        label='Email'
    )
    message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше сообщение...',
            'rows': 5
        }),
        label='Сообщение',
        help_text='Максимум 500 символов'
    )
    
    # Валидация сообщения
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message


class ProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя
    """
    class Meta:
        model = Profile
        fields = ['phone_number', 'bio']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Расскажите о себе...',
                'rows': 4
            }),
        }