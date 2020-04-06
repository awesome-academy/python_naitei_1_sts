from datetime import date

from django.db import models
from django.urls import reverse

from user.models import User
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    STATUS = (
        ('i', 'in progress'),
        ('f', 'finish'),
        ('n', 'not yet'),
    )
    status = models.CharField(choices=STATUS, default='n', max_length=1)
    room_name = models.CharField(max_length=100, default='#', unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    duration = models.PositiveIntegerField()
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Supervisor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.trainer.first_name + " " + self.trainer.last_name


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'subject',)

    def __str__(self):
        return self.course.name + " - " + self.subject.name


class TraineeCourseSubject(models.Model):
    course_subject = models.ForeignKey(CourseSubject, on_delete=models.CASCADE)
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=False)

    STATUS = (
        ('i', 'in progress'),
        ('f', 'finish'),
        ('n', 'not yet'),
    )
    status = models.CharField(choices=STATUS, default='n', max_length=1)

    def __str__(self):
        return self.trainee.username + " - " + self.course_subject.__str__()
