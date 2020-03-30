from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('new/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskUpdateView.as_view(), name='task-detail'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
]
