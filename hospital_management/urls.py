"""hospital_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path("login/",views.login_ ,name = "login"),
    path('after-login/', views.after_login_view),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('staff/', include('staff.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('book-appointment/', views.book_appointment,name = "book_appointment"),
]
