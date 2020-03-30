from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from symbol import parameters

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Subject
from .forms import SubjectCreateForm, SubjectUpdateForm

# Create your views here.
from django.urls import resolve
from django.views import generic, View

from course.forms import CourseTraineeAddForm, SupervisorAddForm, CourseTraineeDeleteForm, SupervisorDeleteForm
from course.models import Course, TraineeCourseSubject, Supervisor, Subject, CourseSubject
from user.models import User


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

    # def post(self, request):


class CourseMemberView(LoginRequiredMixin, View):
    template_name = 'course/course_member.html'

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        course_trainee_list = TraineeCourseSubject.objects.filter(course_subject__course=course)
        supervisor_list = Supervisor.objects.filter(course=course)
        subject_trainer_list = Subject.objects.filter(coursesubject__course=course)
        if request.user.role == 0:
            course_members = set()
            for supervisor in supervisor_list:
                course_members.add(supervisor.trainer)
            for subject_trainer in subject_trainer_list:
                course_members.add(subject_trainer.trainer)
            for course_trainee in course_trainee_list:
                course_members.add(course_trainee.trainee)
            return render(request, self.template_name, {'course_members': course_members, 'course': course})
        else:
            trainee_form = CourseTraineeAddForm()
            trainer_form = SupervisorAddForm()
            course_trainer = set()
            trainee = set()
            for supervisor in supervisor_list:
                course_trainer.add(supervisor.trainer)
            for subject_trainer in subject_trainer_list:
                course_trainer.add(subject_trainer.trainer)
            for course_trainee in course_trainee_list:
                trainee.add(course_trainee.trainee)
            return render(request, self.template_name,
                          {'course_trainee': trainee, 'course_trainer': course_trainer, 'course': course,
                           'trainee_form': trainee_form, 'trainer_form': trainer_form})

    def post(self, request, *args, **kwargs):
        if request.user.role == 1 or request.user.role == 2:
            if request.POST.get('trainee'):
                form = CourseTraineeAddForm(request.POST)
                if form.is_valid():
                    course_subject_list = CourseSubject.objects.filter(course_id=kwargs['pk'])
                    error = False
                    for item in course_subject_list:
                        try:
                            trainee_course_subject = TraineeCourseSubject.objects.get(
                                trainee=form.cleaned_data['trainee'],
                                course_subject=item)
                        except:
                            trainee_course_subject = None
                        if trainee_course_subject is None:
                            trainee_course_subject = TraineeCourseSubject()
                            trainee_course_subject.trainee = form.cleaned_data['trainee']
                            trainee_course_subject.course_subject = item
                            trainee_course_subject.save()
                        else:
                            error = True
                            messages.error(request, 'Sorry this trainee has already been in this course')
                            break
                    if not error:
                        messages.success(request, 'Yay this trainee has successfully added to this course')
            elif request.POST.get('trainer'):
                form = SupervisorAddForm(request.POST)
                if form.is_valid():
                    course = Course.objects.get(pk=kwargs['pk'])
                    try:
                        supervisor = Supervisor.objects.get(course=course, trainer=form.cleaned_data['trainer'])
                    except:
                        supervisor = None
                    if supervisor is None:
                        supervisor = Supervisor()
                        supervisor.course = course
                        supervisor.trainer = form.cleaned_data['trainer']
                        supervisor.save()
                        messages.info(request,
                                      'Yay this trainer has successfully added to this course as supervisor')
                    else:
                        messages.warning(request, 'Sorry this trainer has already been in this course as supervisor')
            elif request.POST.get('trainee_delete'):
                form = CourseTraineeDeleteForm(request.POST)
                if form.is_valid():
                    trainee = User.objects.get(pk=form.cleaned_data['trainee_delete'])
                    course = Course.objects.get(pk=kwargs['pk'])
                    course_subject_list = CourseSubject.objects.filter(course=course)
                    for item in course_subject_list:
                        trainee_course_subject = TraineeCourseSubject.objects.get(trainee=trainee, course_subject=item)
                        trainee_course_subject.delete()
                    messages.success(request, 'Successfully deleted')
            elif request.POST.get('trainer_delete'):
                form = SupervisorDeleteForm(request.POST)
                if form.is_valid():
                    trainer = User.objects.get(pk=form.cleaned_data['trainer_delete'])
                    course = Course.objects.get(pk=kwargs['pk'])
                    supervisor = Supervisor.objects.get(trainer=trainer, course=course)
                    supervisor.delete()
                    messages.info(request, 'Successfully deleted')
        return redirect('course_member', pk=kwargs['pk'])


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
                            WHERE cs.trainer_id = %s OR course_subject.trainer_id = %s'''
            return Subject.objects.raw(raw_query, params=[user.id, user.id])
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
