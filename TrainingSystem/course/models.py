from django.db import models
from user.models import User
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    duration = models.PositiveIntegerField()
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Supervisor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class TraineeCourseSubject(models.Model):
    course_subject = models.ForeignKey(CourseSubject, on_delete=models.CASCADE)
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    is_active = models.BooleanField(default=False)

    STATUS = (
        ('i', 'in progress'),
        ('f', 'finish'),
        ('n', 'not yet'),
    )
    status = models.CharField(choices=STATUS, default='n', max_length=1)
