from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lessons.models import Course, Lesson, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'preview', 'description', 'url', 'course', ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons_in = SerializerMethodField(read_only=True, source='course')

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_in(course):
        return [lesson.__str__() for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ['name', 'preview', 'description', 'count_lessons', 'lessons_in', ]
