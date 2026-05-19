from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-mail')

    def __str__(self):
        return self.username


class Course(models.Model):
    TYPE_CHOICES = [
        ('qualification', 'Повышение квалификации'),
        ('retraining', 'Профессиональная переподготовка'),
        ('safety', 'Охрана труда'),
    ]
    name = models.CharField(max_length=200, verbose_name='Название')
    course_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name='Тип курса'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('invoice', 'Счет на оплату'),
        ('cash', 'Наличные'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс'
    )
    start_date = models.DateField(verbose_name='Дата начала')
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'


class Review(models.Model):
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name='review',
        verbose_name='Заявка'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв к заявке #{self.application_id}'
