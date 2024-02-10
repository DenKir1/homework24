from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson, Payment
from lessons.permissions import IsOwner, IsModerator
from lessons.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('pay_course', 'pay_lesson', 'pay_method', )


class CourseViewSet(ModelViewSet):
    #queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Course.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Course.objects.all()
        else:
            raise PermissionDenied


class LessonListView(ListAPIView):
    #queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            raise PermissionDenied


class LessonCreateView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveView(RetrieveAPIView):
    #queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            raise PermissionDenied


class LessonUpdateView(UpdateAPIView):
    #queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            raise PermissionDenied


class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
