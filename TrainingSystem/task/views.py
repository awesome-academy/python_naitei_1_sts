from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.expressions import RawSQL
from .models import Task
from course.models import CourseSubject, TraineeCourseSubject
from .models import Task, TraineeTask
from .forms import TaskCreateForm, TaskUpdateForm, TaskCreateFormForTrainer
import datetime


# Create your views here.

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        raw_query = '''SELECT task_traineetask.status FROM task_traineetask
                        INNER JOIN task_task tt ON tt.id = task_traineetask.task_id
                        '''
        context['status'] = TraineeTask.objects.raw(raw_query)
        return context

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.role == 0:
            queryset = Task.objects.raw('SELECT task_task.*, task_traineetask.* FROM task_task ' +
                                        'INNER JOIN task_traineetask ON task_task.id = task_traineetask.task_id ' +
                                        'INNER JOIN course_coursesubject ON task_task.course_subject_id = course_coursesubject.id ' +
                                        'INNER JOIN course_traineecoursesubject ON course_coursesubject.id = course_traineecoursesubject.course_subject_id ' +
                                        'INNER JOIN user_user ON task_traineetask.trainee_id = user_user.id ' +
                                        'WHERE course_traineecoursesubject.trainee_id = user_user.id ' +
                                        'AND user_user.is_active = %s ' +
                                        'AND user_user.id = %s', params=[True, user_id])
        else:
            queryset = Task.objects.filter(creator=self.request.user)
        # for task in queryset:
        #     print(task.choice_set.all())
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm

    def get(self, request):
        if request.user.role == 0:
            form = TaskCreateForm(request.user)
            return render(request, 'task/task_form.html', {'form': form})
        else:
            form = TaskCreateFormForTrainer(request.user)
            return render(request, 'task/task_form_trainer.html', {'form': form})

    def post(self, request):
        if request.user.role == 0:
            form = TaskCreateForm(request.user, request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                start_date = form.cleaned_data['start_date']
                due_date = form.cleaned_data['due_date']
                course_subject = form.cleaned_data['course_subject']
                creator = self.request.user
                if form.cleaned_data['type'] == 'r':
                    date = datetime.datetime.today()
                    task = Task(name=name, description=description, start_date=date, due_date=date,
                                course_subject=course_subject, creator=creator, type='r')
                    task.save()
                    trainee_task = TraineeTask(trainee=creator, task=task, status='d')
                    trainee_task.save()
                else:
                    task = Task(name=name, description=description, start_date=start_date, due_date=due_date,
                                course_subject=course_subject, creator=creator, type='t')
                    task.save()
                    trainee_task = TraineeTask(trainee=creator, task=task, status='n')
                    trainee_task.save()
                return redirect('task-list')
            else:
                return render(request, 'task/task_form.html', {'form': form})
        else:
            form = TaskCreateFormForTrainer(request.user, request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                start_date = form.cleaned_data['start_date']
                due_date = form.cleaned_data['due_date']
                course_subject = form.cleaned_data['course_subject']
                trainee = form.cleaned_data['assign']
                creator = self.request.user
                date = datetime.datetime.today()
                task = Task(name=name, description=description, start_date=date, due_date=date,
                            course_subject=course_subject, creator=creator, type='t')
                task.save()
                trainee_task = TraineeTask(trainee=trainee, task=task, status='n')
                trainee_task.save()
                return redirect('task-list')
            else:
                return render(request, 'task/task_form_trainer.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['pk'] = self.get_object().pk
        return kwargs

    def form_valid(self, form):
        status = self.request.POST['status']
        TraineeTask.objects.filter(task_id=self.get_object().pk).update(status=status)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        pk = self.get_object().pk
        form = TaskUpdateForm(pk, request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            TraineeTask.objects.filter(task_id=pk).update(status=status)
            return redirect('task-list')
        else:
            return render(request, 'task/task_update_form.html', {'form': form})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        trainee_task = TraineeTask.objects.filter(task=task, trainee=user)
        trainee_task.delete()
        self.delete(request, *args, *kwargs)
        return HttpResponseRedirect(self.success_url)
