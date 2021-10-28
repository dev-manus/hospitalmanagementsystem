from django.test import TestCase
from django.urls import reverse

from doctor.models import Doctor, Prescription
from django.contrib.auth.models import User


class DoctorTests(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='testuser', password='test@12345')
        Doctor.objects.create(user=user,address='address', contact_no='contact_no')
        Prescription.objects.create(prescription='prescription')

    def test_doctor_login_page(self):
        response = self.client.get(reverse('doctor-login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/login.html')

    def test_doctor_register_page(self):
        response = self.client.get(reverse('doctor-register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/register.html')

    def test_doctor_dashboard_page(self):
        response = self.client.get(reverse('doctor-dashboard'))
        self.assertEquals(response.status_code, 302)

    def test_doctor_view_appointments_page(self):
        response = self.client.get(reverse('view-appointments'))
        self.assertEquals(response.status_code, 302)

    def test_doctor_view_patients_page(self):
        response = self.client.get(reverse('view_patients'))
        self.assertEquals(response.status_code, 302)
