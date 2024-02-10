from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from lessons.models import Payment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    @staticmethod
    def get_payments(user):
        return [payment.__str__() for payment in Payment.objects.filter(user=user)]

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'city', 'is_active', 'payments', ]


class UserOtherSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'city', ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email

        return token
