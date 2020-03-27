from django.urls import path

from course import views

urlpatterns = [
    path('<int:pk>', views.CourseDetailView.as_view(), name='course_detail_trainer'),
]
