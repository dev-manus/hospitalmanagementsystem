from django.db import models
from django.contrib.auth.models import User
from doctor.models import Doctor

# Create your models here.
# CHOICES
sex = [('Male', 'Male'), ('Female', 'Female')]

departments = [
    ('General Physician', 'General Physician'),
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Immunologists', 'Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
]

# Patient model


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    contact_no = models.CharField(max_length=10, null=False)
    symptoms = models.CharField(max_length=200, null=False)
    sex = models.CharField(choices=sex, max_length=6, default='Male')
    department = models.CharField(max_length=30,
                                  choices=departments, default='General Physician')
    assigned_doctor = models.OneToOneField(
        Doctor, null=True, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.laast_name}'

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


# Book appointment model
class Appointment(models.Model):
    patient_id = models.PositiveIntegerField(null=True)
    patient_name = models.CharField(max_length=40, null=True)
    doctor_id = models.PositiveIntegerField(null=True)
    doctor_name = models.CharField(max_length=40, null=True)
    appointment_date = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Patient: {self.patient_id} Doctor: {self.doctor_id}'


# Discharge details model
class DischargeDetails(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.DO_NOTHING)
    doctor = models.OneToOneField(Doctor, on_delete=models.DO_NOTHING)
    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    room_charge = models.PositiveIntegerField(null=False)
    medicine_charge = models.PositiveIntegerField(null=False)
    doctor_charge = models.PositiveIntegerField(null=False)
    other_charge = models.PositiveIntegerField(null=False)
    total_charge = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f'Patient: {self.patient.user.first_name} Doctor: {self.doctor.user.first_name}'
