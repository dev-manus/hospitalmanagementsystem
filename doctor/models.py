from django.db import models
from django.contrib.auth.models import User

sex = [('Male', 'Male'), ('Female', 'Female')]

tenure = [
    ('Trainee', 'Trainee'),
    ('Permanent', 'Permanent'),
    ('Visiting', 'Visiting')
]

departments = [
    ('General Physician', 'General Physician'),
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Immunologists', 'Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
]

# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenure = models.CharField(max_length=10, choices=tenure, default='Visting')
    address = models.CharField(max_length=40)
    contact_no = models.CharField(max_length=10, null=False)
    department = models.CharField(max_length=30,
                                  choices=departments, default='General Physician')
    sex = models.CharField(choices=sex, max_length=6, default='Male')
    salary = models.IntegerField(null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "Dr." + f'{  self.user.first_name} {self.user.last_name} - {self.department}'


# Prescription
class Prescription(models.Model):
    patient_id = models.PositiveIntegerField(null=True)
    patient_name = models.CharField(max_length=40, null=True)
    doctor_id = models.PositiveIntegerField(null=True)
    doctor_name = models.CharField(max_length=40, null=True)
    appointment_date = models.DateField(auto_now=True)
    prescription = models.TextField(max_length=500)
    medicines = models.TextField(max_length=500)

    def __str__(self):
        return f'Patient: {self.patient_id} Doctor: {self.doctor_id}'
