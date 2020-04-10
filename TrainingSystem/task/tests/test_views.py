from django.test import TestCase
from django.urls import reverse
from user.models import User
from course.models import Course, Subject, CourseSubject
from task.models import Task, TraineeTask

class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
        user.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        self.assertRedirects(response, '/login/?next=/task/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-list'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'ho.minh.huy')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'task/task_list.html')
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get('/task/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_list.html')


class TaskCreateViewTrainerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
        user.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-create'))
        self.assertRedirects(response, '/login/?next=/task/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(str(response.context['user']), 'ho.minh.huy')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form_trainer.html')
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get('/task/new/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form_trainer.html')


class TaskCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='tran.quang.khai', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=0)
        user.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-create'))
        self.assertRedirects(response, '/login/?next=/task/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='tran.quang.khai', password='testing321')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(str(response.context['user']), 'tran.quang.khai')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')
        
    def test_view_uses_correct_template(self):
        login = self.client.login(username='tran.quang.khai', password='testing321')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')


class TaskUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
        user.save()
        course = Course.objects.create(name='Naite 14', description='Khoa Naitei thu 14',
                                        status='i', room_name='naitei-14')
        subject = Subject.objects.create(name='Git', description='Mon hoc Git',
                                        duration=3, trainer=user)
        course_subject = CourseSubject.objects.create(course=course, subject=subject)
        Task.objects.create(name='Git Examination', description='Final test after studying Git',
                            start_date='2020-04-09', due_date='2020-04-19', course_subject=course_subject,
                            creator=user, type='t')
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-detail', args=[1]))
        self.assertRedirects(response, '/login/?next=/task/1/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-detail', args=[1]))
        self.assertEqual(str(response.context['user']), 'ho.minh.huy')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_update_form.html')
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get('/task/1/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        login = self.client.login(username='ho.minh.huy', password='testing321')
        response = self.client.get(reverse('task-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_update_form.html')
