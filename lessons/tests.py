
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import User
from lessons.models import Course, Lesson, Subscribe, Payment


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(
            name='test',
            course=self.course,
            owner=self.user,
        )

    def test_get_list_lesson(self):
        """Тестирование получения списка Lesson"""
        response = self.client.get('lessons:lesson_list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        """Тестирование создания Lesson"""
        data = {
            'name': 'test2',
            'description': 'test2'
            }
        response = self.client.post('lessons:lesson_create', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        """Тестирование изменения Lesson"""
        data = {
            'name': 'test3',
            'description': 'test2'
        }
        response = self.client.put('lessons:lesson_update', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Тестирование удаления Lesson"""
        response = self.client.delete('lessons:lesson_update')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.subscription = Subscribe.objects.create(
            user=self.user,
            course=self.course
        )

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        data = {
            'user': self.user.pk,
            'course': self.course.pk
        }

        response = self.client.post('lessons:subscribe', data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class PaymentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.payment = Payment.objects.create(
            user=self.user,
            pay_course=self.course,
            pay_method='transfer',
        )

    def test_payment_list(self):
        """ Проверка списка Payment """
        response = self.client.get(reverse('payment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
