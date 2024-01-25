from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    is_active = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Актуальность')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)
    public_date = models.DateField(auto_now=True, verbose_name='Дата публикации', **NULLABLE)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)
    public_date = models.DateField(auto_now=True, verbose_name='Дата публикации', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name', 'public_date', ]
