from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class TransportType(models.Model):
    
    name = models.CharField(max_length=100, verbose_name='Название')
    icon = models.CharField(max_length=50,  verbose_name='Иконка')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид транспорта'
        verbose_name_plural = 'Виды транспорта'

class Application(models.Model):
    
    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
        ('online', 'Онлайн-платеж'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name='Пользователь'
    )
    transport_type = models.ForeignKey(
        TransportType, 
        on_delete=models.CASCADE,
        verbose_name='Вид транспорта'
    )
    start_date = models.DateField(verbose_name='Дата начала')
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_CHOICES,
        verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name='Статус'
    )
    review = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return f'Заявка #{self.id} - {self.user.username}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

# Create your models here.
