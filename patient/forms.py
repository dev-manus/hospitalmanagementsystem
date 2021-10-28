from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from doctor.models import Doctor
from .models import Appointment, Patient, DischargeDetails


class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'contact_no', 'symptoms', 'sex']


class BookAppointment(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(
        queryset=Doctor.objects.all(), empty_label='Doctor', to_field_name='user_id')

    class Meta:
        model = Appointment
        fields = ['description', 'status',
                  'appointment_date', 'appointment_time']


class DischargeForm(forms.ModelForm):
    class Meta:
        model = DischargeDetails
        fields = ['admitDate', 'releaseDate', 'room_charge',
                  'medicine_charge', 'doctor_charge', 'other_charge']
