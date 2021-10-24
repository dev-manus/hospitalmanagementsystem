from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('register/', patient_register, name='patient-register'),
    path('login/', LoginView.as_view(template_name='patient/login.html', authentication_form=True),
         name='patient-login'),
    path('dashboard/', patient_dashboard, name='patient-dashboard'),
    path('book-appointment/', book_appointment, name='book-appointment'),
    path('appointment-booked/', appointment_booked, name='appointment-booked'),
    path('appointment-history', appointment_history, name='appointment-history'),
    path('get-doctors/', get_all_doctors, name='get-doctors')
]
