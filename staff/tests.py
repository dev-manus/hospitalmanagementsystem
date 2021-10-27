from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

class DoctorTests(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='testuser', password='test@12345')

    def test_staff_login_page(self):
        response = self.client.get(reverse('staff-login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/login.html')

    def test_staff_register_page(self):
        response = self.client.get(reverse('staff-register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/register.html')

    def test_staff_dashboard_page(self):
        response = self.client.get(reverse('staff-dashboard'))
        self.assertEquals(response.status_code, 302)

    def test_staff_unapproved_doctors_page(self):
        response = self.client.get(reverse('unapproved-doctors'))
        self.assertEquals(response.status_code, 302)

    def test_staff_unapproved_appointments_page(self):
        response = self.client.get(reverse('unapproved-appointments'))
        self.assertEquals(response.status_code, 302)

    def test_staff_unapproved_patients_page(self):
        response = self.client.get(reverse('unapproved-patients'))
        self.assertEquals(response.status_code, 302)
        
    
