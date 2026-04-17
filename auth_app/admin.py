from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Это позволит видеть профиль прямо на странице пользователя
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'

# Расширяем стандартный UserAdmin, добавляем в него ProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Перерегистрируем User модель с нашим новым админом
admin.site.unregister(User)  # Отключаем старую регистрацию
admin.site.register(User, CustomUserAdmin)  # Регистрируем с новой

# Отдельно регистрируем Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'bio', 'created_at']
    search_fields = ['user__username', 'user__email']
    
    # Запрещаем удаление профиля отдельно от пользователя
    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление профилей вручную

