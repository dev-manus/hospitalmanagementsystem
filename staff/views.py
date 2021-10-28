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
from patient.forms import DischargeForm


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
    appointmentscount = Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = Appointment.objects.all().filter(status=False).count()
    patientcount = Patient.objects.all().filter(status=True).count()
    pendingpatientcount = Patient.objects.all().filter(status=False).count()

    context = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'apppointmentscount': appointmentscount,
        'pendingappointmentcount': pendingappointmentcount
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
def unapproved_patients_list(request):
    patients = Patient.objects.all().filter(status=False)
    context = {
        'patients': patients
    }
    return render(request, 'staff/patients_list.html', context)


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def approve_doctor(request, pk):
    print(pk)
    doctor = Doctor.objects.get(pk=pk)
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


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def approve_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    patient.status = True
    patient.save()
    return redirect('unapproved-patients')


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def staff_appointment_view(request):
    appointments = Appointment.objects.all().filter(status=True).filter(paid=False)
    context = {
        'appointments': appointments
    }
    return render(request, 'staff/approved_appointments.html', context)

# Generate bill


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def generate_bill(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    patient_id = appointment.patient_id
    doctor_id = appointment.doctor_id
    discharge_form = DischargeForm()
    context = {
        'discharge_form': discharge_form,
        'patient_name': appointment.patient_name,
        'doctor_name': appointment.doctor_name
    }

    if request.method == 'POST':
        discharge_form = DischargeForm(request.POST)

        if discharge_form.is_valid():
            discharge = discharge_form.save(commit=False)
            discharge.doctor = doctor_id
            discharge.patient = patient_id
            discharge.patient_name = appointment.patient_name
            discharge.doctor_name = appointment.doctor_name
            discharge.total_charge = discharge.room_charge + discharge.medicine_charge + \
                discharge.doctor_charge + discharge.other_charge
            appointment.paid = True

            appointment.save()
            discharge.save()
        return redirect('staff-dashboard')
    return render(request, 'staff/discharge_form.html', context)


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def get_approved_doctors(request):
    doctors = Doctor.objects.all().filter(status=True)
    context = {
        'doctors': doctors
    }
    return render(request, 'staff/approved_doctors.html', context)

# Delete appointments


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def delete_appointments(request, pk):
    Appointment.objects.get(pk=pk).delete()
    return redirect('appointment-view')


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def delete_doctor(request, pk):
    Doctor.objects.get(pk=pk).delete()
    return redirect('approved-doctors')


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def delete_patient(request, pk):
    Patient.objects.get(pk=pk).delete()
    return redirect('approved-patients')


@login_required(login_url='staff-login')
@user_passes_test(is_admin, login_url='staff-login')
def get_approved_patients(request):
    patients = Patient.objects.all().filter(status=True)
    context = {
        'patients': patients
    }
    return render(request, 'staff/approved_patients.html', context)
