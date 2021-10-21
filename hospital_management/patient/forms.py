from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from .models import Patient


class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'contact_no', 'symptoms', 'sex']
