from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from taxi.models import Driver


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long")
        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise ValidationError("License number must start with 3 upper case letters")
        if not license_number[3:].isdigit():
            raise ValidationError("License number must end with 5 digits only")
        return license_number


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search car by model"}),
    )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "license_number", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
