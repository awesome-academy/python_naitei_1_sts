from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from course.forms import CourseSubjectFormset, SubjectFormset, SubjectCreateForm
from .forms import UserRegisterForm, UserUpdateForm, UpdateTrainerForm
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from .token import account_activation_token
from course.models import Course, Subject

from django.utils.translation import gettext as _
import json


# Create your views here.


def home(request):
    return render(request, 'user/index.html')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'user.admin_permission'
    model = User
    context_object_name = 'users'
    template_name = 'user/user_list.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            User = form.save(commit=False)
            User.is_active = False
            User.save()
            current_site = get_current_site(request)
            mail_subject = _('Activate your account.')
            message = render_to_string('user/acc_active_email.html', {
                'user': User,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(User.pk)),
                'token': account_activation_token.make_token(User),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse(_('Please confirm your email address to complete the registration'))
            # form.save()
            # messages.success(request, f'Your account has been created! You are now able to log in.')
            # return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        permission = Permission.objects.get(name='login as trainee')
        user.user_permissions.add(permission)
        user.save()

        # login(request, user)
        # return redirect('home')
        return HttpResponse(_('Thank you for your email confirmation. Now you can login your account.'))
    else:
        return HttpResponse(_('Activation link is invalid!'))


@login_required
def profile(request):
    if request.method == "POST":
        update_form = UserUpdateForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, _(f'Your profile has been updated!'))
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)
    context = {'update_form': update_form}
    return render(request, 'user/profile.html', context)


class OtherProfile(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        context = {'user': user}
        return render(request, 'user/other_profile.html', context)


class AprrovedTrainer(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'user.admin_permission'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        update_form = UpdateTrainerForm(instance=user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, _(f'Your profile has been updated!'))

        context = {'update_form': update_form}
        return render(request, 'user/update_trainer.html', context)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        update_form = UpdateTrainerForm(request.POST, instance=user)
        if update_form.is_valid():
            update_form.save()
            role = update_form.cleaned_data['role']
            trainer_permission = Permission.objects.get(name='login as trainer')
            admin_permission = Permission.objects.get(name='login as admin')
            if role == 1:
                user.user_permissions.add(trainer_permission)
                user.user_permissions.remove(admin_permission)
            elif role == 2:
                user.user_permissions.add(trainer_permission)
                user.user_permissions.add(admin_permission)
            else:
                user.user_permissions.remove(admin_permission)
                user.user_permissions.remove(trainer_permission)
            user.save()
            messages.success(request, _(f'Approved trainer success!'))
            return redirect('add-trainer', pk=user.id)


class Search(View):
    def get(self, request):
        keyword = request.GET['keyword']
        course = Course.objects.filter(name__icontains=keyword)
        return render(request, 'user/base.html', {'course': course, 'keyword': keyword}, )


def autocompleteModel(request):
    if request.is_ajax():
        keyword = request.POST.get('inputSearch')
        courses = Course.objects.filter(name__icontains=keyword)
        results = map(lambda x: (x.name, x.get_absolute_url()), courses)
        data = json.dumps(list(results))
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class FormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_show_labels = False


class CourseCreate(generic.CreateView):
    model = Course
    fields = '__all__'
    success_url = reverse_lazy('home')
    template_name = 'user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.POST:

            context['coursesubject'] = CourseSubjectFormset(self.request.POST)
        else:
            context['coursesubject'] = CourseSubjectFormset()
            context['course'] = SubjectFormset()
            context['subjectform'] = SubjectCreateForm()
            context['helper'] = FormsetHelper()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        coursesubject = context['coursesubject']
        with transaction.atomic():
            if coursesubject.is_valid():
                self.object = form.save()
                coursesubject.instance = self.object
                coursesubject.save()
            else:
                messages.error(self.request, 'Subject khong hop le')
                return redirect('home')
        return super().form_valid(form)


class SubjectCreate(generic.CreateView):
    model = Subject
    fields = '__all__'
    success_url = reverse_lazy('home')
    # template_name = 'user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.POST:
            context['course'] = SubjectFormset(self.request.POST)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        course = context['course']
        with transaction.atomic():
            if course.is_valid():
                self.object = form.save()
                course.instance = self.object
                course.save()
            else:
                messages.error(self.request, 'Course khong hop le')
                return redirect('home')
        return super().form_valid(form)
