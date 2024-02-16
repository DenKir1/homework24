from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lessons.models import Course, Lesson, Payment, Subscribe
from lessons.validators import ValidatedUrl


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['is_active', 'user']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'preview', 'description', 'url', 'course', ]
        validators = [ValidatedUrl(field='url'), ValidatedUrl(field='description'), ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField(read_only=True)
    lessons_in = SerializerMethodField(read_only=True, source='course')
    subscribe = SubscribeSerializer(read_only=True, source='subscribe_set', many=True)

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_in(course):
        return [lesson.__str__() for lesson in Lesson.objects.filter(course=course)]

    def get_subscribe(self, obj):
        return obj.subscribe_set.filter(user=self.request.user, course=obj).is_active

    class Meta:
        model = Course
        fields = '__all__'
        validators = [ValidatedUrl(field='description'), ]
