from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def login_user(request):
    """
    Custom login view that:
    - Authenticates user
    - Shows errors when login fails
    - Redirects user based on role
    """
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "accounts/login.html")

    return render(request, 'accounts/login.html')


def redirect_user_by_role(user):
    """Redirect user to dashboard based on their role."""

    role = getattr(user, 'role', None)

    if role == 'cabinet_secretary':
        return redirect('cabinet:home')

    elif role == 'county_director':
        return redirect('county:home')

    elif role == 'subcounty_director':
        return redirect('subcounty:home')

    elif role == 'school_admin':
        return redirect('schools:school_list')

    elif role == 'teacher':
        return redirect('teachers:home')

    # default fallback
    return redirect('home:home')


@require_http_methods(["GET", "POST"])
def logout_user(request):
    """
    Safe logout (GET + POST).
    Fixes Method Not Allowed error.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')
