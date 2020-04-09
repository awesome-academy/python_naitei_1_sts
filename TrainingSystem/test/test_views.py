from django.test import TestCase
from django.urls import reverse

from user.models import User
from task.models import Task, TraineeTask
from course.models import Course, Supervisor, CourseSubject, Subject, TraineeCourseSubject
from django.utils import timezone
import datetime
import uuid
from django.contrib.auth.models import Permission

password = 'pbkdf2_sha256$180000$WHO5XRxXtQGK$W+vbMG8IK4MfaJgsIkx+RYJtKSqboBDobcJ/ragPYZA='


class UserNotLogIn(TestCase):
    @classmethod
    def setUpTestData(cls):
        number = 10

        for user_id in range(number):
            User.objects.create(
                username=f'Hunghm{user_id}',
                password=password,
                first_name=f'Hung{user_id}',
                last_name=f'Hoang{user_id}',
                role=0,
            )

        for course_id in range(number):
            Course.objects.create(
                name=f'naitei{course_id}',
                description='course',
                status='i',
                room_name=f'room{course_id}',
            )
        for subject_id in range(number):
            Subject.objects.create(
                name=f'git{subject_id}',
                description='subject',
                duration=10,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_list_user_before_login(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_other_user_before_login(self):
        response = self.client.get(reverse('view-profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_add_trainer_before_login(self):
        response = self.client.get(reverse('add-trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_trainer_detail_course_before_login(self):
        response = self.client.get(reverse('course_detail_trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_detail_course_before_login(self):
        response = self.client.get(reverse('course_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_delete_course_before_login(self):
        response = self.client.get(reverse('course_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_create_course_before_login(self):
        response = self.client.get(reverse('course_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_list_course_before_login(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_detail_subject_before_login(self):
        response = self.client.get(reverse('subject-detail-trainee', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_detail_subject_trainer_before_login(self):
        response = self.client.get(reverse('subject-detail-trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_delete_subject_before_login(self):
        response = self.client.get(reverse('subject-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_create_subject_before_login(self):
        response = self.client.get(reverse('subject-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_list_course_before_login(self):
        response = self.client.get(reverse('subject-list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class TestUserLogin(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password=password)
        test_user2 = User.objects.create_user(username='testuser2', password=password)
        test_user3 = User.objects.create_user(username='testuser3', password=password)
        test_user4 = User.objects.create_user(username='testuser4', password=password)
        test_user1.save()
        test_user2.save()
        test_user3.save()
        test_user4.save()
        trainee_permission = Permission.objects.get(name='login as trainee')
        test_user2.user_permissions.add(trainee_permission)
        trainer_permission = Permission.objects.get(name='login as trainer')
        test_user3.user_permissions.add(trainer_permission)
        admin_permission = Permission.objects.get(name='login as admin')
        test_user4.user_permissions.add(admin_permission)
        test_user1.save()
        test_user2.save()
        test_user3.save()
        test_user4.save()
        self.other_user = test_user1
        for course_id in range(10):
            Course.objects.create(
                name=f'naitei{course_id}',
                description='course',
                status='i',
                room_name=f'room{course_id}',
            )
        for subject_id in range(10):
            Subject.objects.create(
                name=f'git{subject_id}',
                description='subject',
                duration=10,
                trainer=test_user3
            )

    def test_view_list_user_after_login(self):
        login = self.client.login(username='testuser1', password=password)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 403)

    def test_view_list_user_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 403)

    def test_view_list_user_by_admin(self):
        login = self.client.login(username='testuser4', password=password)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

    def test_template_view_list_user_by_admin(self):
        login = self.client.login(username='testuser4', password=password)
        response = self.client.get(reverse('user-list'))
        self.assertTemplateUsed(response, 'user/user_list.html')

    def test_view_other_user(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('view-profile', kwargs={'pk': self.other_user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_template_view_other_user(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('view-profile', kwargs={'pk': self.other_user.pk}))
        self.assertTemplateUsed(response, 'user/other_profile.html')

    def test_approve_trainer_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('add-trainer', kwargs={'pk': self.other_user.pk}))
        self.assertEqual(response.status_code, 403)

    def test_approve_trainer_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('add-trainer', kwargs={'pk': self.other_user.pk}))
        self.assertEqual(response.status_code, 403)

    def test_approve_trainer_by_admin(self):
        login = self.client.login(username='testuser4', password=password)
        response = self.client.get(reverse('add-trainer', kwargs={'pk': self.other_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update_trainer.html')

    def test_approve_trainer_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('course_detail_trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/course_detail.html')

    def test_view_course_detail_by_user(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('course_detail_trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/course_detail.html')

    def test_view_subject_detail_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('subject-detail-trainee', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_subject_trainer_detail_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('subject-detail-trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_subject_trainer_detail_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('subject-detail-trainer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_access_course_create_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('course_create'))
        self.assertEqual(response.status_code, 403)

    def test_access_course_delete_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('course_delete',kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_access_course_create_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('course_create'))
        self.assertEqual(response.status_code, 200)

    def test_access_course_delete_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('course_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_access_subject_delete_by_trainee(self):
        login = self.client.login(username='testuser2', password=password)
        response = self.client.get(reverse('subject-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_access_subject_delete_by_trainer(self):
        login = self.client.login(username='testuser3', password=password)
        response = self.client.get(reverse('subject-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
