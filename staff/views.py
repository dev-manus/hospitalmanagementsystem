from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from doctor.models import Doctor
from patient.models import Appointment, Patient
from .forms import StaffRegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def staff_register(request):
    print(User.objects.first())
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return redirect('staff-login')
    form = StaffRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'staff/register.html', context)


@login_required(login_url='/staff/login')
@user_passes_test(is_admin, login_url='/staff/login')
def staff_dashboard(request):
    doctors = Doctor.objects.all().order_by('-id')
    patients = Patient.objects.all().order_by('-id')
    doctorcount = Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = Doctor.objects.all().filter(status=False).count()
    appointmentscount = Appointment.objects.all().filter(status=False).count()
    patientcount = Patient.objects.all().filter(status=True).count()
    pendingpatientcount = Patient.objects.all().filter(status=False).count()

    context = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'apppointmentscount': appointmentscount
    }
    return render(request, 'staff/dashboard.html', context)


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def unapproved_doctors_list(request):
    doctors = Doctor.objects.all().filter(status=False)
    context = {
        'doctors': doctors
    }
    return render(request, 'staff/doctors_list.html', context)


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def unapproved_appointments_list(request):
    appointments = Appointment.objects.all().filter(status=False)
    context = {
        'appointments': appointments
    }
    return render(request, 'staff/appointments_list.html', context)


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def approve_doctor(request, pk):
    print(pk)
    doctor = Doctor.objects.get(user_id=pk)
    doctor.status = True
    doctor.save()
    return redirect('unapproved-doctors')


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def approve_appointment(request, pk):
    print(pk)
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = True
    appointment.save()
    return redirect('unapproved-appointments')
