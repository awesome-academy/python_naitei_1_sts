from django.test import TestCase
from user.models import User
from course.models import Course, Subject, CourseSubject
from task.models import Task, TraineeTask

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
        course = Course.objects.create(name='Naite 14', description='Khoa Naitei thu 14',
                                        status='i', room_name='naitei-14')
        subject = Subject.objects.create(name='Git', description='Mon hoc Git',
                                        duration=3, trainer=user)
        course_subject = CourseSubject.objects.create(course=course, subject=subject)
        Task.objects.create(name='Git Examination', description='Final test after studying Git',
                            start_date='2020-04-09', due_date='2020-04-19', course_subject=course_subject,
                            creator=user, type='t')

    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_start_date_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('start_date').verbose_name
        self.assertEquals(field_label, 'start date')

    def test_due_date_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('due_date').verbose_name
        self.assertEquals(field_label, 'due date')
    
    def test_course_subject_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('course_subject').verbose_name
        self.assertEquals(field_label, 'course subject')
    
    def test_creator_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('creator').verbose_name
        self.assertEquals(field_label, 'creator')
    
    def test_type_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_description_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('description').max_length
        self.assertEquals(max_length, 500)

    def test_object_name_is_self_name(self):
        task = Task.objects.get(id=1)
        expected_object_name = task.name
        self.assertEquals(expected_object_name, str(task))


class TraineeTaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
        course = Course.objects.create(name='Naite 14', description='Khoa Naitei thu 14',
                                        status='i', room_name='naitei-14')
        subject = Subject.objects.create(name='Git', description='Mon hoc Git',
                                        duration=3, trainer=user)
        course_subject = CourseSubject.objects.create(course=course, subject=subject)
        task = Task.objects.create(name='Git Examination', description='Final test after studying Git',
                            start_date='2020-04-09', due_date='2020-04-19', course_subject=course_subject,
                            creator=user, type='t')
        TraineeTask.objects.create(trainee=user, task=task, status='n')

    def test_trainee_label(self):
        trainee_task = TraineeTask.objects.get(id=1)
        field_label = trainee_task._meta.get_field('trainee').verbose_name
        self.assertEquals(field_label, 'trainee')

    def test_task_label(self):
        trainee_task = TraineeTask.objects.get(id=1)
        field_label = trainee_task._meta.get_field('task').verbose_name
        self.assertEquals(field_label, 'task')

    def test_status_label(self):
        trainee_task = TraineeTask.objects.get(id=1)
        field_label = trainee_task._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_object_name_is_self_name(self):
        trainee_task = TraineeTask.objects.get(id=1)
        expected_object_name = f'{trainee_task.task.id}'
        self.assertEquals(expected_object_name, str(trainee_task))
