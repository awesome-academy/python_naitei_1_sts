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
