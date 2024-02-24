import stripe

from config import settings
from lessons.models import Payment, Lesson

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
        success_url='https://example.com/success',
        line_items=[{'price': price.id, 'quantity': 1, }],
        mode='payment',

    )

    return session


def retrieve_stripe(session_id):
    """ Получаем ответ Stripe"""
    return stripe.checkout.Session.retrieve(session_id)
