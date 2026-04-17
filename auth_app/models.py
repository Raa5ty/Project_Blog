from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Расширение стандартной модели User
    Добавляет дополнительные поля для пользователя
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Номер телефона'
    )
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name='О себе'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания профиля'
    )
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

# Сигнал для автоматического создания Profile при создании User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматически сохраняет профиль при сохранении пользователя"""
    instance.profile.save()
