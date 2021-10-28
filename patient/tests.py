from django.test import TestCase
from django.urls import reverse
import datetime
from doctor.models import Doctor
from patient.models import Patient, Appointment,DischargeDetails
from doctor.models import Doctor
from django.contrib.auth.models import User


class PatientTests(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='testuser', password='test@12345')
        pat = Patient.objects.create(user=user,address='address', contact_no='contact_no')
        doc = Doctor.objects.create(user=user,address='address', contact_no='contact_no')
        Appointment.objects.create()
        DischargeDetails.objects.create(patient=pat,
            doctor=doc,
            admitDate=datetime.date.today(),
            releaseDate=datetime.date.today(),
            room_charge=10,
            medicine_charge=10,
            doctor_charge=10,
            other_charge=10,
            total_charge=10)

    def test_patient_login_page(self):
        response = self.client.get(reverse('patient-login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient/login.html')

    def test_patient_register_page(self):
        response = self.client.get(reverse('patient-register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient/register.html')

    def test_patient_appointment_history_page(self):
        response = self.client.get(reverse('appointment-history'))
        self.assertEquals(response.status_code, 302)

    def test_patient_get_doctors_page(self):
        response = self.client.get(reverse('get-doctors'))
        self.assertEquals(response.status_code, 302)

    def test_patient_view_prescriptions_page(self):
        response = self.client.get(reverse('view-prescriptions'))
        self.assertEquals(response.status_code, 302)
