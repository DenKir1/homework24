from django.contrib.auth.models import AbstractUser
from django.db import models

from lessons.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}
ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]

PAY_CHOICES = [
    ('cash', 'наличные'),
    ('transfer', 'перевод'),
]

SUCCESS_CHOICES = [
    (True, 'Оплачено'),
    (False, 'Не оплачено'),
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


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    pay_date = models.DateTimeField(auto_now=True, verbose_name='Дата оплаты', **NULLABLE)
    pay_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    pay_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    price_summ = models.FloatField(verbose_name='Цена', **NULLABLE)
    pay_method = models.CharField(default='transfer', choices=PAY_CHOICES, verbose_name='Способ оплаты')
    is_success = models.BooleanField(default=False, choices=SUCCESS_CHOICES, verbose_name='Оплачено')

    def __str__(self):
        return f"{self.pay_date} {self.user} {self.pay_method}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['pay_date', ]
