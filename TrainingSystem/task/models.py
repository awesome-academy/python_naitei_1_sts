from django.db import models
from course.models import CourseSubject
from user.models import User
# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_date = models.DateField()
    due_date = models.DateField()
    course_subject = models.ForeignKey(CourseSubject, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    TYPE = (
        ('r', 'report'),
        ('t', 'task'),
    )
    type = models.CharField(choices=TYPE, default='t', max_length=1)

    def __str__(self):
        return self.name


class TraineeTask(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    STATUS = (
        ('d', 'done'),
        ('i', 'in progress'),
        ('n', 'new'),
    )

    status = models.CharField(choices=STATUS, default='n', max_length=1)

    def __str__(self):
        return f'{self.task.id}'
