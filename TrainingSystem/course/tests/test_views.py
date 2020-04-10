from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from course.models import Course, Subject, CourseSubject
from user.models import User


class CourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_trainer_1 = User.objects.create_user(username='testtrainer1', password='1X<ISRUkw+tuK', role=1)
        test_trainer_2 = User.objects.create_user(username='testtrainer2', password='1X<ISRUkw+tuK', role=1)
        test_admin = User.objects.create_user(username='testadmin', password='1X<ISRUkw+tuK', role=2)
        numbers_of_courses = 10

        for course_id in range(numbers_of_courses):
            Course.objects.create(name=f'name {course_id}', description=f'description {course_id}', status='n',
                                  room_name=f'room-{course_id}')

        numbers_of_subject_trainer1 = 5
        for subject_id in range(numbers_of_subject_trainer1):
            Subject.objects.create(name=f'name {subject_id}', description=f'description {subject_id}', duration=1,
                                   trainer=test_trainer_1)

        numbers_of_subject_trainer2 = 5
        for subject_id in range(numbers_of_subject_trainer2):
            Subject.objects.create(name=f'name {subject_id}', description=f'description {subject_id}', duration=1,
                                   trainer=test_trainer_2)

        numbers_of_course_subject = 5
        for course_subject_id in range(numbers_of_course_subject):
            CourseSubject.objects.create(course=Course.objects.get(id=course_subject_id + 1),
                                         subject=Subject.objects.get(id=course_subject_id + 1))
        for course_subject_id in range(numbers_of_course_subject):
            CourseSubject.objects.create(course=Course.objects.get(id=course_subject_id + 6),
                                         subject=Subject.objects.get(id=course_subject_id + 6))

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('course_list'))
        self.assertRedirects(response, '/login/?next=/course/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('course_list'))

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/course_list.html')

    def test_list_course_logged_in_trainer(self):
        login = self.client.login(username='testtrainer1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 5)

    def test_list_course_logged_in_admin(self):
        login = self.client.login(username='testadmin', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 10)


class SubjectCreateViewTest(TestCase):
    def setUp(self):
        test_trainer1 = User.objects.create_user(username='testtrainer1', password='1X<ISRUkw+tuK', role=1)
        test_trainer2 = User.objects.create_user(username='testtrainer2', password='1X<ISRUkw+tuK', role=1)
        test_trainer1.save()
        test_trainer2.save()

        permission = Permission.objects.get(name='login as trainer')
        test_trainer1.user_permissions.add(permission)
        test_trainer1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('subject-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/?next=/course/subject/new/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testtrainer2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('subject-create'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission(self):
        login = self.client.login(username='testtrainer1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('subject-create'))
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        login = self.client.login(username='testtrainer1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('subject-create'))
        self.assertTemplateUsed(response, 'course/subject_form.html')
