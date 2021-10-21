from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import *

# Create your views here.


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

        return HttpResponseRedirect('patient/login/')
    return render(request, 'patient/register.html', context=view_context)


# Patient's dashboard
@login_required(login_url='patient-login')
def patient_dashboard(request):
    return render(request, 'patient/dashboard.html')
