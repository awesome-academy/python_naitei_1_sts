from django.db import models
from user.models import User
from course.models import Course


# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(course):
        return Message.objects.order_by('timestamp').filter(course=course)[:10]
