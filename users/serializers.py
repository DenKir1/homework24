from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    @staticmethod
    def get_payments(user):
        return [payment.__str__() for payment in Payment.objects.filter(user=user)]

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'city', 'is_active', 'payments', ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
