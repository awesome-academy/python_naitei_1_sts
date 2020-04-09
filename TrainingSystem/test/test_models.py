from datetime import date

from django.test import TestCase
from user.models import User
from task.models import Task, TraineeTask
from course.models import Course, Supervisor, CourseSubject, Subject, TraineeCourseSubject


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='hunghm1', first_name='Hoang', last_name='Hung', phone="0334814467", role=0)
        trainer = User.objects.create(username='hunghm2', first_name='Le', last_name='Minh', phone="0334814467", role=1)
        task = Task.objects.create(name='task1', description="task1", start_date=date.today(), due_date=date.today(),
                                   type="r", creator=user)
        TraineeTask.objects.create(trainee=user, task=task, status='n')
        course = Course.objects.create(name='naitei', description='khoa naitei', status='i', room_name='naitei')
        subject = Subject.objects.create(name='git', description='git subject', duration=10, trainer=trainer)
        supervisor = Supervisor.objects.create(course=course, trainer=trainer)

        course_subject = CourseSubject.objects.create(course=course, subject=subject)



    def test_user_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_user_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 30)

    def test_user_phone_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('phone').max_length
        self.assertEquals(max_length, 15)

    def test_task_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_task_description_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('description').max_length
        self.assertEquals(max_length, 500)

    def test_task_object_name(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task.name}'
        self.assertEquals(expected_object_name, str(task))

    def test_trainee_task_status_max_length(self):
        trainee_task = TraineeTask.objects.get(id=1)
        max_length = trainee_task._meta.get_field('status').max_length
        self.assertEquals(max_length, 1)

    def test_trainee_task_object_name(self):
        trainee_task = TraineeTask.objects.get(id=1)
        expected_object_name = f'{trainee_task.task.id}'
        self.assertEquals(expected_object_name, str(trainee_task))

    def test_course_description_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_course_object_name(self):
        course = Course.objects.get(id=1)
        expected_object_name = f'{course.name}'
        self.assertEquals(expected_object_name, str(course))

    def test_course_absolute_url(self):
        course = Course.objects.get(id=1)
        expected_url = course.get_absolute_url()
        self.assertEquals(expected_url, '/course/1')

    def test_subject_description_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_subject_object_name(self):
        subject = Subject.objects.get(id=1)
        expected_object_name = f'{subject.name}'
        self.assertEquals(expected_object_name, str(subject))

    def test_supervisor_object_name(self):
        supervisor = Supervisor.objects.get(id=1)
        expected_object_name = f'{supervisor.trainer.first_name} {supervisor.trainer.last_name}'
        self.assertEquals(expected_object_name, str(supervisor))

    def test_course_subject_object_name(self):
        course_subject = CourseSubject.objects.get(id=1)
        expected_object_name = f'{course_subject.course.name} - {course_subject.subject.name}'
        self.assertEquals(expected_object_name, str(course_subject))

