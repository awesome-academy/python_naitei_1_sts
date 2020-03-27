from django.urls import path

from course import views
from course.views import SubjectListView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView, SubjectDetailView

urlpatterns = [
    path('<int:pk>', views.CourseDetailView.as_view(), name='course_detail_trainer'),
    path('subjects', SubjectListView.as_view(), name='subject-list'),
    path('subject/new/', SubjectCreateView.as_view(), name='subject-create'),
    path('subject/<int:pk>/', SubjectUpdateView.as_view(), name='subject-detail-trainer'),
    path('subject/<int:pk>/detail', SubjectDetailView.as_view(), name='subject-detail-trainee'),
    path('subject/<int:pk>/delete', SubjectDeleteView.as_view(), name='subject-delete'),
    path('<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/members/', views.CourseMemberView.as_view(), name='course_member'),
]
