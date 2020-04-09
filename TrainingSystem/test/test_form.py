import datetime

from django.test import TestCase
from django.utils import timezone

from user.forms import UserRegisterForm, UserUpdateForm, UpdateTrainerForm
from task.forms import TaskCreateForm, TaskCreateFormForTrainer, TaskUpdateForm


class UserFormTest(TestCase):
    # all def for test label form
    def test_register_form_field_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['username'].label == 'Tên đăng nhập' or  form.fields['username'].label == 'Username')

    def test_user_update_form_field_label(self):
        form = UserUpdateForm()
        self.assertTrue(form.fields['username'].label == 'Tên đăng nhập' or form.fields['username'].label == 'Username')

    def test_update_trainer_form_field_label(self):
        form = UpdateTrainerForm()
        self.assertTrue(form.fields['phone'].label == 'Số điện thoại' or form.fields['phone'].label == 'Phone')

