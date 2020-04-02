from django.contrib import admin

# Register your models here.
from course.models import Course, Subject, Supervisor, CourseSubject, TraineeCourseSubject

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Supervisor)
admin.site.register(CourseSubject)

@admin.register(TraineeCourseSubject)
class TraineeCourseSubjectAdmin(admin.ModelAdmin):
    list_display = ('course_subject', 'trainee', 'start_date', 'is_active', 'status')
    list_filter = ('course_subject', 'trainee', 'is_active', 'status')
