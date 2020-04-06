from django import forms
from django.conf import settings
from .models import Task, TraineeTask
from course.models import CourseSubject, TraineeCourseSubject
from django.db.models.expressions import RawSQL
from user.models import User
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


class TaskCreateFormForTrainer(TaskCreateForm):
    assign = forms.ModelChoiceField(queryset=User.objects.filter(role=0))

    def __init__(self, *args, **kwargs):
        super(TaskCreateFormForTrainer, self).__init__(*args, **kwargs)
        raw_query = '''SELECT course_coursesubject.id FROM course_coursesubject 
                        LEFT JOIN course_supervisor cs ON cs.course_id = course_coursesubject.course_id
                        LEFT JOIN course_subject cs1 ON cs1.id = course_coursesubject.subject_id
                        WHERE cs1.trainer_id = %s
                        OR cs.trainer_id = %s'''
        self.fields['course_subject'].queryset = CourseSubject.objects.filter(id__in=RawSQL(raw_query, params=[self.user.id, self.user.id]))

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('type', 'creator',)


class TaskUpdateForm(forms.ModelForm):
    STATUS = (
        ('n', 'new'),
        ('i', 'in progress'),
        ('d', 'done'),
    )
    status = forms.ChoiceField(choices=STATUS)

    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        print(pk)
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        print(TraineeTask.objects.filter(task_id=pk).values_list('status', flat=True).first())
        self.fields['status'].initial = TraineeTask.objects.filter(task_id=pk).values_list('status', flat=True).first()

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator', 'type',)
