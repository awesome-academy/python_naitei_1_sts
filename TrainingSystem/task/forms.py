from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator',)

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('creator', 'type',)
