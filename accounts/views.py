# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.urls import reverse

from .forms import LoginForm


# ============================================================
# SAFE ?next= REDIRECT
# ============================================================
def _get_safe_next(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if not next_url:
        return None

    allowed_hosts = {request.get_host()}
    allowed_hosts.update(getattr(settings, "ALLOWED_HOSTS", []))

    if url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts=allowed_hosts,
        require_https=request.is_secure()
    ):
        return next_url
    return None


# ============================================================
# ROLE-BASED REDIRECTION
# ============================================================
def redirect_user_by_role(user):

    role = getattr(user, "role", None)

    role_map = {
        "cabinet_secretary": "cabinet:home",
        "county_director": "county:home",
        "subcounty_director": "subcounty:home",
        "school_admin": "schools:school_list",
        "teacher": "teachers:home",
        "learner": "learners:home",
    }

    if role in role_map:
        return redirect(role_map[role])

    return redirect("home:home")


# ============================================================
# UNIVERSAL LOGIN
# ============================================================
def login_user(request):

    # Already logged in → no need to show login page
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    next_safe = _get_safe_next(request)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.error(request, "Your account is inactive. Contact admin.")
                return render(request, "accounts/login.html", {
                    "form": form,
                    "next": next_safe
                })

            login(request, user)
            return redirect(next_safe) if next_safe else redirect_user_by_role(user)

        # Invalid credentials → Django adds errors automatically
        messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {
        "form": form,
        "next": next_safe
    })


# ============================================================
# LOGOUT
# ============================================================
@require_http_methods(["GET", "POST"])
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("accounts:login")
