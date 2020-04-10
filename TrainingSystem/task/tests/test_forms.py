from django.test import TestCase
from user.models import User
from task.forms import TaskCreateForm, TaskCreateFormForTrainer, TaskUpdateForm


class TaskCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
    
    def test_task_create_form_name_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')
    
    def test_task_create_form_description_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['description'].label == None or form.fields['description'].label == 'Description')
    
    def test_task_create_form_start_date_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['start_date'].label == None or form.fields['start_date'].label == 'start date')
    
    def test_task_create_form_due_date_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['due_date'].label == None or form.fields['due_date'].label == 'due date')

    def test_task_create_form_course_subject_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['course_subject'].label == None or form.fields['course_subject'].label == 'course subject')
    
    def test_task_create_form_type_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateForm(user)
        self.assertTrue(form.fields['type'].label == None or form.fields['type'].label == 'Type')


class TaskCreateFormForTrainerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
    
    def test_task_create_form_for_trainer_assign_field_label(self):
        user = User.objects.get(id=1)
        form = TaskCreateFormForTrainer(user)
        self.assertTrue(form.fields['assign'].label == None or form.fields['assign'].label == 'assign')


class TaskUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='ho.minh.huy', password='testing321',
                                    dob='1990-01-01', phone='0123456789', role=1)
    
    def test_task_update_form_status_field_label(self):
        user = User.objects.get(id=1)
        form = TaskUpdateForm(user.id)
        self.assertTrue(form.fields['status'].label == None or form.fields['status'].label == 'Status')
