from symbol import parameters

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Subject
from .forms import SubjectCreateForm, SubjectUpdateForm

# Create your views here.
from django.views import generic

from course.models import Course


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course


class SubjectListView(generic.ListView):
    model = Subject
    context_object_name = 'subjects'

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            raw_query = '''SELECT course_subject.* FROM course_subject
                           INNER JOIN course_coursesubject cc on course_subject.id = cc.subject_id
                           INNER JOIN course_traineecoursesubject ct on cc.id = ct.course_subject_id
                           WHERE ct.is_active = %s 
                           AND trainee_id = %s'''
            return Subject.objects.raw(raw_query, params=[True, user.id])
        else:
            raw_query = '''SELECT course_subject.* FROM course_subject
                            INNER JOIN course_coursesubject cc on course_subject.id = cc.subject_id
                            INNER JOIN course_course cc2 on cc.course_id = cc2.id
                            INNER JOIN course_supervisor cs on cc2.id = cs.course_id
                            WHERE cs.trainer_id = %s'''
            return Subject.objects.raw(raw_query, params=[user.id])
            return None


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'user.trainer_permission'

    model = Subject
    form_class = SubjectCreateForm

    def post(self, request):
        form = SubjectCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            duration = form.cleaned_data['duration']
            trainer = self.request.user
            subject = Subject(name=name, description=description, duration=duration, trainer=trainer)
            subject.save()
            return redirect('subject-list')


class SubjectUpdateView(generic.UpdateView):
    model = Subject
    form_class = SubjectUpdateForm
    template_name_suffix = '_update_form'


class SubjectDetailView(generic.DetailView):
    model = Subject


class SubjectDeleteView(generic.DeleteView):
    model = Subject
    success_url = reverse_lazy('subject-list')
