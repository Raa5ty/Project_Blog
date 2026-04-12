from django.contrib import admin

# Register your models here.
# Для регистрации модели Post в админке, нужно импортировать её и зарегистрировать
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Поля, которые будут видны в списке
    list_filter = ('created_at',)           # Фильтр по дате
    search_fields = ('title', 'content')    # Поиск по заголовку и содержанию
    ordering = ('-created_at',)             # Сортировка: новые сверху