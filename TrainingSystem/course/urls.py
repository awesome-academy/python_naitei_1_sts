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
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('new/', views.CourseCreateView.as_view(), name='course_create'),
    path('course-subject/create/', views.CourseSubjectCreateView.as_view(), name='course_subject_create'),
    path('course-subject/', views.CourseSubjectListView.as_view(), name='course_subject_list'),
    path('course-subject/<int:pk>/delete/', views.CourseSubjectDeleteView.as_view(), name='course_subject_delete'),
    path('course-subject/<int:pk>/edit/', views.CourseSubjectUpdateView.as_view(), name='course-subject-update'),
    path('course-subject/<int:pk>/active/', views.course_subject_active, name='course-subject-active'),
    path('course-subject/<int:pk>/deactive/', views.course_subject_deactive, name='course-subject-deactive'),
]
