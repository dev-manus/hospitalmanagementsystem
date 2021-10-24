# Check if the user is doctor, admin or user

from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

# View function after logging in


def after_login_view(request):
    user = request.user
    if is_doctor(user):
        return HttpResponseRedirect('/doctor/dashboard')
    elif is_patient(user):
        return HttpResponseRedirect('/patient/dashboard')
    elif is_admin(user):
        return HttpResponseRedirect('/staff/dashboard')


def index(request):
    return render(request, "hospital_management/index.html")


def book_appointment(request):
    user = request.user

    # user is authonticated, so it can book appointment directly
    if user.is_authenticated:
        return redirect('/patient/book-appointment')

    # user isn't authonticated, it will be prompted to login first
    # then from there , he will be directed to book appointment
    else:
        print("here")
        return render(request, "hospital_management/login.html", {
            next: "book_appt"
        })


def login_(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if is_doctor(user):
                return HttpResponseRedirect('/doctor/dashboard')
            elif is_admin(user):
                return HttpResponseRedirect('/staff/dashboard')
            return HttpResponseRedirect('/patient/dashboard')
        else:
            return render(request, "hospital_management/login.html", {
                "message": "Invalid username and/or password.",
                "login_active": True,
            })
    else:
        return render(request, "hospital_management/login.html", {
            "login_active": True,
        })
