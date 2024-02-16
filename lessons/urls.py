from django.urls import path

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, PaymentViewSet, LessonListView, LessonCreateView, LessonRetrieveView, \
    LessonUpdateView, LessonDeleteView, SubscribeAPIView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('subscribe/<int:pk>/', SubscribeAPIView.as_view(), name='subscribe'),

] + router.urls
