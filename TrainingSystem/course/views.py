from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
# Create your views here.
from django.views import generic, View

from course.forms import CourseTraineeAddForm, SupervisorAddForm, CourseTraineeDeleteForm, SupervisorDeleteForm, \
    CourseUpdateForm, CourseCreateForm, CourseSubjectCreateForm, CourseSubjectUpdateForm
from course.models import Course, TraineeCourseSubject, Supervisor, Subject, CourseSubject
from user.models import User
from .forms import SubjectCreateForm, SubjectUpdateForm


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(kwargs)
        user = self.request.user
        course = kwargs['object']
        if user.role == 0:
            try:
                trainee_course_subject = get_object_or_404(TraineeCourseSubject, trainee=user,
                                                           course_subject__course=course,
                                                           is_active=True)
            except:
                trainee_course_subject = None
            if trainee_course_subject is not None:
                context['status'] = trainee_course_subject
        course_update_form = CourseUpdateForm()
        context['course_update_form'] = course_update_form
        return context

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        form = CourseUpdateForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.description = form.cleaned_data['description']
            course.status = form.cleaned_data['status']
            course.save()
        return redirect("course_detail", pk=kwargs['pk'])


class CourseMemberView(LoginRequiredMixin, View):
    template_name = 'course/course_member.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
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
                            trainee_course_subject = get_object_or_404(TraineeCourseSubject,
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
                            messages.error(request, _('Sorry this trainee has already been in this course'))
                            break
                    if not error:
                        messages.success(request, _('Yay this trainee has successfully added to this course'))
            elif request.POST.get('trainer'):
                form = SupervisorAddForm(request.POST)
                if form.is_valid():
                    course = get_object_or_404(Course, pk=kwargs['pk'])
                    try:
                        supervisor = get_object_or_404(Supervisor, course=course, trainer=form.cleaned_data['trainer'])
                    except:
                        supervisor = None
                    if supervisor is None:
                        supervisor = Supervisor()
                        supervisor.course = course
                        supervisor.trainer = form.cleaned_data['trainer']
                        supervisor.save()
                        messages.info(request,
                                      _('Yay this trainer has successfully added to this course as supervisor'))
                    else:
                        messages.warning(request, _('Sorry this trainer has already been in this course as supervisor'))
            elif request.POST.get('trainee_delete'):
                form = CourseTraineeDeleteForm(request.POST)
                if form.is_valid():
                    trainee = get_object_or_404(User, pk=form.cleaned_data['trainee_delete'])
                    course = get_object_or_404(Course, pk=kwargs['pk'])
                    course_subject_list = CourseSubject.objects.filter(course=course)
                    for item in course_subject_list:
                        trainee_course_subject = get_object_or_404(TraineeCourseSubject, trainee=trainee,
                                                                   course_subject=item)
                        trainee_course_subject.delete()
                    messages.success(request, _('Successfully deleted'))
            elif request.POST.get('trainer_delete'):
                form = SupervisorDeleteForm(request.POST)
                if form.is_valid():
                    trainer = get_object_or_404(User, pk=form.cleaned_data['trainer_delete'])
                    course = get_object_or_404(Course, pk=kwargs['pk'])
                    supervisor = get_object_or_404(Supervisor, trainer=trainer, course=course)
                    supervisor.delete()
                    messages.info(request, _('Successfully deleted'))
        return redirect('course_member', pk=kwargs['pk'])


class SubjectListView(LoginRequiredMixin, generic.ListView):
    model = Subject
    context_object_name = 'subjects'

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            raw_query = '''SELECT DISTINCT course_subject.* FROM course_subject
                           LEFT JOIN course_coursesubject cc on course_subject.id = cc.subject_id
                           LEFT JOIN course_traineecoursesubject ct on cc.id = ct.course_subject_id
                           WHERE ct.is_active = %s 
                           AND trainee_id = %s'''
            return Subject.objects.raw(raw_query, params=[True, user.id])
        else:
            raw_query = '''SELECT DISTINCT course_subject.* FROM course_subject
                            LEFT JOIN course_coursesubject cc on course_subject.id = cc.subject_id
                            LEFT JOIN course_course cc2 on cc.course_id = cc2.id
                            LEFT JOIN course_supervisor cs on cc2.id = cs.course_id
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


class SubjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Subject
    form_class = SubjectUpdateForm
    template_name_suffix = '_update_form'


class SubjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Subject


class SubjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Subject
    success_url = reverse_lazy('subject-list')


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'

    def get_queryset(self):
        user = self.request.user
        course = set()
        if user.role == 0:
            trainee_course_subject_list = TraineeCourseSubject.objects.filter(trainee=user)
            course_subject_list = set()
            for trainee_course_subject in trainee_course_subject_list:
                course_subject_list.add(trainee_course_subject.course_subject)
            for course_subject in course_subject_list:
                course.add(course_subject.course)
            return course
        elif user.role == 1:
            supervisor_list = Supervisor.objects.filter(trainer=user)
            for supervisor in supervisor_list:
                course.add(supervisor.course)
            subject_list = Subject.objects.filter(trainer=user)
            for subject in subject_list:
                course_subject_list = CourseSubject.objects.filter(subject=subject)
                for course_subject in course_subject_list:
                    course.add(course_subject.course)
        elif user.role == 2:
            course = Course.objects.all()
        return course


class CourseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')


class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Course
    form_class = CourseCreateForm
    success_url = reverse_lazy('course_list')

    def post(self, request, *args, **kwargs):
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect('course_list')


class CourseSubjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = CourseSubject
    form_class = CourseSubjectCreateForm

    def post(self, request, *args, **kwargs):
        form = CourseSubjectCreateForm(request.POST)
        if form.is_valid():
            course_subject = form.save(commit=False)
            course_subject.save()
            return redirect('course_subject_list')


class CourseSubjectListView(LoginRequiredMixin, generic.ListView):
    model = CourseSubject
    context_object_name = 'course_subjects'
    template_name = 'course/coursesubject_list.html'

    def get_queryset(self):
        user = self.request.user
        course_subject_list = set()
        if user.role == 1:
            supervisor_list = Supervisor.objects.filter(trainer=user)
            course_list = set()
            for supervisor in supervisor_list:
                course_list.add(supervisor.course)
            for course in course_list:
                course_subject_list_1 = CourseSubject.objects.filter(course=course)
                for course_subject in course_subject_list_1:
                    course_subject_list.add(course_subject)
            subject_list = Subject.objects.filter(trainer=user)
            for subject in subject_list:
                course_subject_list_2 = CourseSubject.objects.filter(subject=subject)
                for course_subject in course_subject_list_2:
                    course_subject_list.add(course_subject)
        elif user.role == 2:
            course_subject_list = CourseSubject.objects.all()
        return course_subject_list


class CourseSubjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CourseSubject
    success_url = reverse_lazy('course_subject_list')


class CourseSubjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CourseSubject
    success_url = reverse_lazy('course_subject_list')
    template_name = 'course/coursesubject_update.html'
    form_class = CourseSubjectUpdateForm


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        raw_query = '''SELECT DISTINCT user_user.username FROM user_user
                    INNER JOIN course_traineecoursesubject ct on ct.trainee_id = user_user.id
                    INNER JOIN course_coursesubject ccs on ccs.id = ct.course_subject_id
                    INNER JOIN course_course cc on cc.id = ccs.course_id '''
        trainee = User.objects.filter(username__in=RawSQL(raw_query, params=[]))
        result = ""
        for tr in trainee:
            result += tr.username
        # print(result)
        # context['trainee'] = trainee
        context['username'] = result
        # print(context['username'])
        return context


def course_subject_active(request, pk):
    course_subject = get_object_or_404(CourseSubject, pk=pk)
    trainee_course_subject_list = TraineeCourseSubject.objects.filter(course_subject=course_subject)
    trainee_course_subject_active = TraineeCourseSubject.objects.filter(course_subject__course=course_subject.course,
                                                                        is_active=True)
    for t in trainee_course_subject_active:
        t.is_active = False
        t.status = 'f'
        t.save()
    for trainee_course_subject in trainee_course_subject_list:
        trainee_course_subject.is_active = True
        trainee_course_subject.status = 'i'
        trainee_course_subject.save()
    return redirect('course_detail', course_subject.course.pk)


def course_subject_deactive(request, pk):
    user = request.user
    course_subject = get_object_or_404(CourseSubject, pk=pk)
    trainee_course_subject = get_object_or_404(TraineeCourseSubject, trainee=user, course_subject=course_subject)
    trainee_course_subject.is_active = False
    trainee_course_subject.status = 'f'
    trainee_course_subject.save()
    return redirect('course_detail', course_subject.course.pk)
