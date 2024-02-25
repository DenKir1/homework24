from django.db import models

from users.models import User

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


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    price_course = models.FloatField(verbose_name='Цена', **NULLABLE)
    is_active = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Актуальность')
    public_date = models.DateField(auto_now=True, verbose_name='Дата публикации', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['name', 'public_date', ]


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью', **NULLABLE)
    url = models.URLField(verbose_name='Ссылка', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, verbose_name='Курс')
    is_active = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Актуальность')
    public_date = models.DateField(auto_now=True, verbose_name='Дата публикации', **NULLABLE)
    price_lesson = models.FloatField(verbose_name='Цена', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name} - {self.description} - URL={self.url} - PRICE={self.price_lesson}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name', 'public_date', ]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    pay_date = models.DateTimeField(auto_now=True, verbose_name='Дата оплаты', **NULLABLE)
    pay_url = models.CharField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
    session = models.CharField(max_length=400, verbose_name='Сессия для оплаты в Stripe', **NULLABLE)
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


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь подписки', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс подписки', **NULLABLE)

    is_active = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Актуальность')
    public_date = models.DateField(auto_now=True, verbose_name='Дата подписки', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['public_date', 'course', 'user', ]
