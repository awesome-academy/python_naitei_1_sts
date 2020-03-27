from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from course.models import Course


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
