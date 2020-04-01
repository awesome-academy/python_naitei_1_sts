from django import forms
from .models import Subject


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ('trainer',)


class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ('trainer',)
from django.db.models import Q

from course.models import TraineeCourseSubject, Supervisor
from user.models import User


class CourseTraineeAddForm(forms.ModelForm):
    trainee = forms.ModelChoiceField(queryset=User.objects.filter(role=0))

    class Meta:
        model = TraineeCourseSubject
        fields = ['trainee']


class SupervisorAddForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(queryset=User.objects.filter(~Q(role=0)))

    class Meta:
        model = Supervisor
        fields = ['trainer']


class SupervisorDeleteForm(forms.Form):
    trainer_delete = forms.IntegerField()


class CourseTraineeDeleteForm(forms.Form):
    trainee_delete = forms.IntegerField()
