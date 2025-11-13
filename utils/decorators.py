# utils/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    """
    Decorator to restrict access to users with specific roles.

    Usage:
        @role_required(['teacher', 'school_admin'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
                return redirect('accounts:login')

            # Get user's role
            role = getattr(user, 'role', None)

            if role in allowed_roles or user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to access this page.")
                return redirect('home:home')

        return wrapper
    return decorator
