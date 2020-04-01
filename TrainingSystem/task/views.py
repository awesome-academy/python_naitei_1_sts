from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models.expressions import RawSQL
from .models import Task
from course.models import CourseSubject, TraineeCourseSubject
from .models import Task, TraineeTask
from .forms import TaskCreateForm, TaskUpdateForm
import datetime

# Create your views here.

class TaskListView(generic.ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Task.objects.filter(id__in=RawSQL('SELECT task_task.id FROM task_task ' + 
                                                    'INNER JOIN task_traineetask ON task_task.id = task_traineetask.task_id ' +
                                                    'INNER JOIN course_coursesubject ON task_task.course_subject_id = course_coursesubject.id ' +
                                                    'INNER JOIN course_traineecoursesubject ON course_coursesubject.id = course_traineecoursesubject.course_subject_id ' +
                                                    'INNER JOIN user_user ON task_traineetask.trainee_id = user_user.id ' +
                                                    'WHERE course_traineecoursesubject.trainee_id = user_user.id ' +
                                                    'AND user_user.is_active = %s ' +
                                                    'AND course_traineecoursesubject.is_active = %s ' +
                                                    'AND user_user.id = %s', params=[True, True, user_id]))
        return queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm

    def post(self, request):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            due_date = form.cleaned_data['due_date']
            course_subject = form.cleaned_data['course_subject']
            creator = self.request.user
            if form.cleaned_data['type'] == 'r':
                date = datetime.datetime.today()
                task = Task(name=name, description=description, start_date=date, due_date=date, course_subject=course_subject, creator=creator, type='r')
                task.save()
                trainee_task = TraineeTask(trainee=creator, task=task, status='d')
                trainee_task.save()
            else:
                task = Task(name=name, description=description, start_date=start_date, due_date=due_date, course_subject=course_subject, creator=creator, type='t')
                task.save()
                trainee_task = TraineeTask(trainee=creator, task=task, status='n')
                trainee_task.save()
            return redirect('task-list')
        else:
            return render(request, 'task/task_form.html', {'form': form})


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
