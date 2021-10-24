from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('register/', views.staff_register, name='staff-register'),
    path('login/', LoginView.as_view(template_name='staff/login.html'),
         name='staff-login'),

]
