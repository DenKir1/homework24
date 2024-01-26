from django.contrib import admin

from users.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'pay_date', 'pay_course', 'pay_lesson', 'price_summ', 'pay_method', 'is_success']
    list_filter = ['user', 'pay_date']
    search_fields = ('pay_date', 'user')
