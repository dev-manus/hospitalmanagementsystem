from django import forms
from django.contrib.auth.models import User
from .models import Doctor

# Form for doctor


class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'contact_no', 'sex', 'department']
