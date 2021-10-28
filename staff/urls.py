from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', staff_dashboard, name='staff-dashboard'),
    path('register/', staff_register, name='staff-register'),
    path('login/', LoginView.as_view(template_name='staff/login.html'),
         name='staff-login'),
    path('unapproved-doctors/', unapproved_doctors_list, name='unapproved-doctors'),
    path('unapproved-appointments/',
         unapproved_appointments_list, name='unapproved-appointments'),
    path('unapproved-patients/', unapproved_patients_list,
         name='unapproved-patients'),
    path('approve-doctor/<int:pk>', approve_doctor, name='approve-doctor'),
    path('approve-appointment/<int:pk>',
         approve_appointment, name='approve-appointment'),
    path('approve-patient/<int:pk>', approve_patient, name='approve-patient'),
    path('appointments', staff_appointment_view, name='appointment-view'),
    path('generate-bill/<int:pk>', generate_bill, name='generate-bill'),
    path('doctors/', get_approved_doctors, name='approved-doctors'),
    path('patients/', get_approved_patients, name='approved-patients'),
    path('delete-doctor/<int:pk>', delete_doctor, name='delete-doctor'),
    path('delete-patient/<int:pk>', delete_patient, name='delete-patient'),
    path('delete-appointment/<int:pk>',
         delete_appointments, name='delete-appointment')
]
