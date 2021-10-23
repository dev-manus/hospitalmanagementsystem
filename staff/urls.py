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
    path('approve-doctor/<int:pk>', approve_doctor, name='approve-doctor'),
    path('approve-appointment/<int:pk>',
         approve_appointment, name='approve-appointment'),
]
