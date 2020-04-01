from django.contrib import admin
from .models import Task, TraineeTask

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'due_date', 'course_subject', 'creator', 'type')
    list_filter = ('name', 'course_subject', 'creator', 'type')


@admin.register(TraineeTask)
class TraineeTaskAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'task', 'status')
    list_filter = ('trainee', 'task', 'status')
