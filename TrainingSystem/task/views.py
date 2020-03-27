from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskCreateForm, TaskUpdateForm

# Create your views here.

class TaskListView(generic.ListView):
    model = Task
    context_object_name = 'tasks'


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
