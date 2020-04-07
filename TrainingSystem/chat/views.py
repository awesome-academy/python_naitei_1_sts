import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from course.models import Course, TraineeCourseSubject, Supervisor, Subject


def index(request):
    return render(request, 'chat/index.html', {})


@login_required
def room(request, room_name):
    username = request.user.username
    course = get_object_or_404(Course, room_name=room_name)
    course_trainee_list = TraineeCourseSubject.objects.filter(course_subject__course=course)
    supervisor_list = Supervisor.objects.filter(course=course)
    subject_trainer_list = Subject.objects.filter(coursesubject__course=course)
    course_members = set()
    for supervisor in supervisor_list:
        course_members.add(supervisor.trainer)
    for subject_trainer in subject_trainer_list:
        course_members.add(subject_trainer.trainer)
    for course_trainee in course_trainee_list:
        course_members.add(course_trainee.trainee)

    if request.user in course_members:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(username)),

        })
    else:
        return redirect('home')
