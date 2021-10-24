from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

from doctor.models import Doctor
from patient.models import Appointment, Patient
from .forms import DoctorUserForm, DoctorForm
from django.http import HttpResponseRedirect

# Create your views here.


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def doctor_register(request):
    user_form = DoctorUserForm()
    doctor_form = DoctorForm()
    view_context = {'user_form': user_form, 'doctor_form': doctor_form}

    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            # Adding doctor to the DOCTOR group
            doctor_group = Group.objects.get_or_create(name='DOCTOR')
            doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('/doctor/login')
    return render(request, 'doctor/register.html', context=view_context)


# Doctor's dashboard
@login_required(login_url='doctor-login')
@user_passes_test(is_doctor, login_url='doctor-login')
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
    patients = Patient.objects.all()

    appointment_count = len(appointments)
    patient_count = len(patients)
    view_context = {
        'doctor': doctor,
        'appointments': appointments,
        'appointment_count': appointment_count,
        'patient_count': patient_count,
        'patients': patients
    }
    return render(request, 'doctor/dashboard.html', context=view_context)

# View appointments


@login_required(login_url='doctor-login')
@user_passes_test(is_doctor, login_url='doctor-login')
def view_appointments(request):
    appointments = Appointment.objects.all().filter(
        doctor_id=request.user.id).filter(status=True)
    view_context = {
        'appointments': appointments
    }
    return render(request, 'doctor/view_appointments.html', context=view_context)


@login_required(login_url='doctor-login')
@user_passes_test(is_doctor, login_url='doctor-login')
def view_patients(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    patients = Patient.objects.all().filter(department=doctor.department)
    view_context = {
        'patients': patients
    }
    return render(request, 'doctor/patient_list.html', context=view_context)
