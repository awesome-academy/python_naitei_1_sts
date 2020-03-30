from django import forms
from django.conf import settings
from .models import Task
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
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator',)


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator', 'type',)
