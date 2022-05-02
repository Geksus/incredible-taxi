from django.test import TestCase

from taxi.forms import NewUserForm


class NewUserFormTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "unforgivable1254",
            "password2": "unforgivable1254",
            "email": "",
            "license_number": "AAA12345",
        }
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
