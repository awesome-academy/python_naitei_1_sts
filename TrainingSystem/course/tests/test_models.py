from django.test import TestCase

from course.models import Course, Subject
from user.models import User


class TestCourseClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(name='test course', description='1X<ISRUkw+tuK')

    def test_name_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_status_label(self):
        course = Course.objects.get(id=1)
        field_name = course._meta.get_field('status').verbose_name
        self.assertEquals(field_name, 'status')

    def test_room_name_label(self):
        course = Course.objects.get(id=1)
        field_name = course._meta.get_field('room_name').verbose_name
        self.assertEquals(field_name, 'room name')

    def test_name_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_description_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_status_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('status').max_length
        self.assertEquals(max_length, 1)

    def test_status_default_value(self):
        course = Course.objects.get(id=1)
        expected_status = 'n'
        self.assertEquals(expected_status, course.status)

    def test_object_name_is_name(self):
        course = Course.objects.get(id=1)
        expected_object_name = course.name
        self.assertEquals(expected_object_name, str(course))

    def test_get_absolute_url(self):
        course = Course.objects.get(id=1)
        self.assertEquals(course.get_absolute_url(), '/course/1')


class TestSubjectClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_trainer = User.objects.create_user(username='testtrainer', password='1X<ISRUkw+tuK',  role=1)
        Subject.objects.create(name='test subject', description='', duration=1, trainer=test_trainer)

    def test_name_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_duration_label(self):
        subject = Subject.objects.get(id=1)
        field_name = subject._meta.get_field('duration').verbose_name
        self.assertEquals(field_name, 'duration')

    def test_trainer_label(self):
        subject = Subject.objects.get(id=1)
        field_name = subject._meta.get_field('trainer').verbose_name
        self.assertEquals(field_name, 'trainer')

    def test_name_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_description_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_name(self):
        subject = Subject.objects.get(id=1)
        expected_object_name = subject.name
        self.assertEquals(expected_object_name, str(subject))
