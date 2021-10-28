from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *
from patient.views import check_username

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
        path('register/check_username/<usr>',check_username, name='check_username'),
]
