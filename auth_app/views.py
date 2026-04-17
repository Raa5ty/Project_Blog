from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, MessageForm, ProfileForm
from .models import Profile


class RegisterView(CreateView):
    """Регистрация нового пользователя"""
    form_class = RegistrationForm
    template_name = 'auth_app/register.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        """Если пользователь уже авторизован - перенаправляем на главную"""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """При успешной регистрации - авторизуем пользователя"""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        # messages.success(self.request, f'Добро пожаловать, {user.username}! Регистрация успешна.')
        return response


class CustomLoginView(LoginView):
    """Авторизация пользователя"""
    form_class = LoginForm
    template_name = 'auth_app/login.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        """Если пользователь уже авторизован - перенаправляем на главную"""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """При успешной авторизации"""
        # messages.success(self.request, f'С возвращением, {form.cleaned_data.get("username")}!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Перенаправление после успешного входа"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')


# def logout_view(request):
#     logout(request)
#     return redirect('home')

class CustomLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        """При выходе показываем сообщение"""
        # if request.user.is_authenticated:
        #     messages.info(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """Просмотр и редактирование профиля пользователя"""
    model = Profile
    form_class = ProfileForm
    template_name = 'auth_app/profile.html'
    success_url = reverse_lazy('profile')
    login_url = '/auth/login/'  # URL для перенаправления неавторизованных
    
    def get_object(self, queryset=None):
        """Получаем профиль текущего пользователя"""
        return self.request.user.profile
    
    def form_valid(self, form):
        """При успешном обновлении профиля"""
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


class MessageView(FormView):
    """Страница отправки сообщения"""
    form_class = MessageForm
    template_name = 'auth_app/message.html'
    success_url = reverse_lazy('message')
    
    def form_valid(self, form):
        """При успешной отправке сообщения"""
        # Здесь можно добавить логику отправки email или сохранения в БД
        messages.success(self.request, 'Ваше сообщение отправлено! Спасибо за обратную связь.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """При ошибках валидации"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)
