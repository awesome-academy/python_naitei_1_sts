from django import forms
from .models import Subject, Course, CourseSubject
from django.db.models import Q
from django.forms import inlineformset_factory

from course.models import TraineeCourseSubject, Supervisor
from user.models import User


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ('trainer',)


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


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        if ' ' in room_name:
            raise forms.ValidationError("Room name can't contain space")
            # self.add_error('room_name', "Room name can't contain space")
        return room_name


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        if ' ' in room_name:
            raise forms.ValidationError("Room name can't contain space")
        return room_name


class CourseSubjectCreateForm(forms.ModelForm):
    class Meta:
        model = CourseSubject
        fields = '__all__'


class CourseSubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = CourseSubject
        fields = '__all__'


CourseSubjectFormset = inlineformset_factory(Course, CourseSubject, fields=('subject',), extra=1)
SubjectFormset = inlineformset_factory(Subject, CourseSubject, fields=('course',), extra=1)
