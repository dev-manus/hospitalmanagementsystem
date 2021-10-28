from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

from doctor.models import Prescription
from .forms import *
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def patient_register(request):
    user_form = PatientUserForm()
    patient_form = PatientForm()
    view_context = {
        'user_form': user_form,
        'patient_form': patient_form
    }

    if(request.method == 'POST'):
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            # Adding patient to PATIENT group
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)

        return HttpResponseRedirect('/login/')
    return render(request, 'patient/register.html', context=view_context)


# Patient's dashboard
@login_required(login_url='login')
def patient_dashboard(request):
    patient = Patient.objects.get(user_id=request.user.id)

    view_context = {
        'patient': patient
    }
    return render(request, 'patient/dashboard.html', context=view_context)

# Book appointment


@login_required(login_url='login')
@user_passes_test(is_patient, login_url='login')
def book_appointment(request):
    patient = Patient.objects.get(user_id=request.user.id)
    appointment_form = BookAppointment()
    view_context = {'appointment_form': appointment_form,
                    'patient': patient}

    if request.method == 'POST':
        appointment_form = BookAppointment(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.doctor_id = request.POST.get('doctor_id')
            appointment.patient_id = request.user.id
            appointment.doctor_name = User.objects.get(
                id=request.POST.get('doctor_id')).first_name
            appointment.patient_name = request.user.first_name
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect('/patient/appointment-booked')
    return render(request, 'patient/book_appointment.html', context=view_context)


@login_required(login_url='patient-login')
@user_passes_test(is_patient, login_url='patient-login')
def appointment_booked(request):
    appointment = Appointment.objects.all().filter(
        patient_id=request.user.id).last()

    view_context = {
        'appointment': appointment
    }
    return render(request, 'patient/appointment_booked.html', context=view_context)


@login_required(login_url='patient-login')
@user_passes_test(is_patient, login_url='patient-login')
def appointment_history(request):
    patient = Patient.objects.get(user_id=request.user.id)
    appointments = Appointment.objects.all().filter(
        patient_id=request.user.id).filter(status=True)

    view_context = {
        'appointments': appointments,
        'patient' : patient,
    }
    return render(request, 'patient/appointment_history.html', context=view_context)


@login_required(login_url='patient-login')
@user_passes_test(is_patient, login_url='patient-login')
def get_all_doctors(request):
    doctors = Doctor.objects.all().filter(status=True)

    view_context = {
        'doctors': doctors
    }
    return render(request, 'patient/doctors_list.html', context=view_context)


@login_required(login_url='login')
@user_passes_test(is_patient, login_url='login')
def get_prescriptions(request):
    prescriptions = Prescription.objects.all().filter(patient_id=request.user.id)
    # doctor = Doctor.objects.get(user_id=prescriptions.doctor_id)
    # patient = Patient.objects.get(user_id=prescriptions.patient_id)

    view_context = {
        'prescriptions': prescriptions
    }
    return render(request, 'patient/prescriptions.html', context=view_context)


# Utility functions
def check_username(request, usr):
    username_exists = User.objects.filter(username__iexact=usr).exists()
    return HttpResponse(username_exists)


def view_profile(request):
    patient = Patient.objects.get(user_id=request.user.id)

    view_context = {
        'patient': patient
    }
    return render(request, 'patient/profile.html', context=view_context)
