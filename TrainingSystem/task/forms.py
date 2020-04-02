from django import forms
from django.conf import settings
from .models import Task
from course.models import CourseSubject, TraineeCourseSubject
from django.db.models.expressions import RawSQL
from .widgets import DatePickerInput

class TaskCreateForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=DatePickerInput()
    )
    due_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=DatePickerInput()
    )
    course_subject = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        raw_query = '''SELECT course_coursesubject.id FROM course_coursesubject
                        INNER JOIN course_traineecoursesubject ct ON course_coursesubject.id = ct.course_subject_id
                        WHERE ct.is_active = %s
                        AND ct.trainee_id = %s'''
        self.fields['course_subject'].queryset = CourseSubject.objects.filter(id__in=RawSQL(raw_query, params=[True, self.user.id]))

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator',)


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator', 'type',)
