from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from doctor.models import Doctor
from patient.models import Patient
from .forms import StaffRegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.


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


class StaffLoginView(LoginView):
    template_name = 'staff/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('staff-dashboard')


def staff_dashboard(request):
    doctors = Doctor.objects.all().order_by('-id')
    patients = Patient.objects.all().order_by('-id')
    doctorcount = Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = Doctor.objects.all().filter(status=False).count()

    patientcount = Patient.objects.all().filter(status=True).count()
    pendingpatientcount = Patient.objects.all().filter(status=False).count()

    context = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
    }
    return render(request, 'staff/dashboard.html', context)
