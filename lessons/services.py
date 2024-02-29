from datetime import datetime, timedelta

import stripe
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from config import settings
from lessons.models import Payment, Subscribe, Lesson, Course

stripe.api_key = settings.STRIPE_API_KEY


def get_stripe(serializer: Payment):
    """ Внешнее API Stripe оплата курса или урока"""
    product_name = serializer.pay_course.name if serializer.pay_course else serializer.pay_lesson.name
    product_price = serializer.pay_course.price_course if serializer.pay_course else serializer.pay_lesson.price_lesson
    product = stripe.Product.create(name=product_name)
    price = stripe.Price.create(
        unit_amount=product_price * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[{'price': price.id, 'quantity': 1, }],
        mode='payment',

    )

    return session


def retrieve_stripe(session_id):
    """ Получаем ответ Stripe"""
    return stripe.checkout.Session.retrieve(session_id)


@shared_task
def subscriptions_mailing(course_id=0, lesson_id=0):
    for subscription in Subscribe.objects.filter(course_id=course_id):
        now = datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        update_date = Course.objects.filter(pk=course_id).first().update_date
        expired = now - update_date > timedelta(hours=4)
        if lesson_id and expired:
            send_mail(
                subject='Изменение/добавление урока',
                message=f'Урок {Lesson.objects.get(pk=lesson_id)} изменен/добавлен.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )
        else:
            send_mail(
                subject='Изменение курса',
                message=f'Курс "{subscription.course}" изменен.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )
