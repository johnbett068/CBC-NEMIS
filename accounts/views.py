from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    """
    Unified login for all roles:
    - Cabinet Secretary
    - County Director
    - Subcounty Director
    - School Admin
    - Teacher
    """
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def redirect_user_by_role(user):
    """Redirects user to the appropriate dashboard based on their role."""
    role = getattr(user, 'role', None)

    if role == 'cabinet_secretary':
        return redirect('cabinet:home')  # create cabinet app later
    elif role == 'county_director':
        return redirect('county:home')  # create county app later
    elif role == 'subcounty_director':
        return redirect('subcounty:home')  # create subcounty app later
    elif role == 'school_admin':
        return redirect('schools:school_list')
    elif role == 'teacher':
        return redirect('teachers:home')
    else:
        return redirect('home:home')


def logout_user(request):
    """Logout any authenticated user."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')
