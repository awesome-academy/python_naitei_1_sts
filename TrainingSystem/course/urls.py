from django.urls import path

from course import views
from course.views import SubjectListView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView, SubjectDetailView

urlpatterns = [
    path('<int:pk>', views.CourseDetailView.as_view(), name='course_detail_trainer'),
    path('subjects', SubjectListView.as_view(), name='subject-list'),
    path('new/', SubjectCreateView.as_view(), name='subject-create'),
    path('<int:pk>/', SubjectUpdateView.as_view(), name='subject-detail-trainer'),
    path('<int:pk>/detail', SubjectDetailView.as_view(), name='subject-detail-trainee'),
    path('<int:pk>/delete', SubjectDeleteView.as_view(), name='subject-delete'),
]
