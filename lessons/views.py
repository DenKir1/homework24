from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson, Payment, Subscribe
from lessons.paginators import LessonPagination
from lessons.permissions import IsOwner, IsModerator
from lessons.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscribeSerializer
from lessons.services import get_stripe, retrieve_stripe, subscriptions_mailing


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('pay_course', 'pay_lesson', 'pay_method', )
    pagination_class = LessonPagination

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Payment.objects.filter(user=self.request.user)
        elif self.request.user.is_staff:
            return Payment.objects.all()
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        if payment.pay_method == 'transfer':
            session = get_stripe(payment)
            payment.pay_url = session.url
            payment.session = session.id
        payment.save()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj.session:
            session = retrieve_stripe(obj.session)
            if session.payment_status == 'paid' and session.status == 'complete':
                obj.is_success = True
                obj.save()

        return obj


class CourseViewSet(ModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonPagination

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

    def perform_update(self, serializer):
        course_id = serializer.save(owner=self.request.user).id
        subscriptions_mailing.delay(course_id=course_id)


class LessonListView(ListAPIView):
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]
    pagination_class = LessonPagination

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
        course_id = new_lesson.course.id
        lesson_id = new_lesson.id
        subscriptions_mailing.delay(course_id=course_id, lesson_id=lesson_id)


class LessonRetrieveView(RetrieveAPIView):
    # queryset = Lesson.objects.all()
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
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        course_id = serializer.save().course.id
        lesson_id = serializer.save().id
        subscriptions_mailing.delay(course_id=course_id, lesson_id=lesson_id)


class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class SubscribeAPIView(APIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()

    def post(self, *args, **kwargs):
        user = self.request.user
        # print(self.request.__dict__)
        course_id = self.kwargs['pk']
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscribe.objects.filter(user=user, course=course_item).first()

        # Если подписка у пользователя на этот курс есть - (де)/активируем ее
        if subs_item:
            if subs_item.is_active:
                subs_item.is_active = False
                subs_item.save()
                message = 'подписка деактивирована'
            else:
                subs_item.is_active = True
                subs_item.save()
                message = 'подписка активирована'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(user=user, course=course_item)
            message = 'подписка создана'
        # Возвращаем ответ в API
        return Response({"message": message})
