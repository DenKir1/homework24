from django.urls import path

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDeleteView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListCreateView.as_view(), name='lesson_list_create'),
    path('lesson/<int:pk>/', LessonRetrieveUpdateDeleteView.as_view(), name='lesson_retrieve_update_destroy'),

] + router.urls
