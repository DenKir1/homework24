from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}
ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    verify_code = models.CharField(max_length=15, verbose_name='Код верификации почты', **NULLABLE)
    verify_phone = models.CharField(max_length=15, verbose_name='Код верификации телефона', **NULLABLE)
    is_active = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Почта активирована')
    is_verify = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Номер телефона верифицирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email', 'city', ]