from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_dashboard, name='staff-dashboard'),
    path('register/', views.staff_register, name='staff-register'),
    path('login/', views.StaffLoginView.as_view(),name='staff-login'),
    
]
