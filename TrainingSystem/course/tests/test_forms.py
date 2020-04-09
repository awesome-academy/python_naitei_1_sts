from django.test import TestCase

from course.forms import CourseCreateForm, CourseUpdateForm


class CourseCreateFormTest(TestCase):
    def test_course_create_form_name_label(self):
        form = CourseCreateForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')

    def test_course_create_form_description_label(self):
        form = CourseCreateForm()
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_course_create_form_status_label(self):
        form = CourseCreateForm()
        self.assertTrue(form.fields['status'].label is None or form.fields['status'].label == 'Status')

    def test_course_create_form_room_name_label(self):
        form = CourseCreateForm()
        self.assertTrue(form.fields['room_name'].label is None or form.fields['room_name'].label == 'Room name')

    def test_course_create_form_room_name_with_blank_space(self):
        form = CourseCreateForm(
            data={'room_name': 'a b', 'name': 'name test', 'description': 'description test', 'status': 'n'})
        self.assertFalse(form.is_valid())

    def test_course_create_form_description_null_allow(self):
        form = CourseCreateForm(data={'name': 'test name', 'description': '', 'status': 'n', 'room_name': 'a'})
        self.assertTrue(form.is_valid())

    def test_course_create_form_status_value_not_satisfied(self):
        form = CourseCreateForm(
            data={'name': 'test name', 'description': 'test description', 'status': 'a', 'room_name': 'a'})
        self.assertFalse(form.is_valid())


class CourseUpdateFormTest(TestCase):
    def test_course_update_form_name_label(self):
        form = CourseUpdateForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')

    def test_course_update_form_description_label(self):
        form = CourseUpdateForm()
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_course_update_form_status_label(self):
        form = CourseUpdateForm()
        self.assertTrue(form.fields['status'].label is None or form.fields['status'].label == 'Status')

    def test_course_update_form_room_name_label(self):
        form = CourseUpdateForm()
        self.assertTrue(form.fields['room_name'].label is None or form.fields['room_name'].label == 'Room name')

    def test_course_update_form_room_name_with_blank_space(self):
        form = CourseUpdateForm(
            data={'room_name': 'a b', 'name': 'name test', 'description': 'description test', 'status': 'n'})
        self.assertFalse(form.is_valid())

    def test_course_update_form_description_null_allow(self):
        form = CourseUpdateForm(data={'name': 'test name', 'description': '', 'status': 'n', 'room_name': 'a'})
        self.assertTrue(form.is_valid())

    def test_course_update_form_status_value_not_satisfied(self):
        form = CourseUpdateForm(
            data={'name': 'test name', 'description': 'test description', 'status': 'a', 'room_name': 'a'})
        self.assertFalse(form.is_valid())
