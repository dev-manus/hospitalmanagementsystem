# Check if the user is doctor, admin or user

from django.shortcuts import redirect


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
        return redirect('/doctor/dashboard')
    elif is_patient(user):
        return redirect('/patient/dashboard')
    elif is_admin(user):
        return redirect('/admin/dashboard')
