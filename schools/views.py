from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from location.models import SubCounty, Ward
from .models import School
from .forms import SchoolForm
from utils.decorators import role_required


@login_required
@role_required(['school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def school_list(request):
    user = request.user
    role = getattr(user, 'role', None)

    # Filter schools based on user role
    if role == 'cabinet_secretary':
        schools = School.objects.all()
    elif role == 'county_director':
        schools = School.objects.filter(county=user.county)
    elif role == 'subcounty_director':
        schools = School.objects.filter(sub_county=user.sub_county)
    else:  # school_admin
        schools = School.objects.filter(id=getattr(user, 'school_id', None))

    context = {
        'dashboard_title': "Schools",
        'schools': schools,
        'breadcrumb': [
            {"name": "Home", "url": '/'},
            {"name": "Schools", "url": '#'}
        ]
    }
    return render(request, 'schools/school_list.html', context)


@login_required
@role_required(['school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def school_detail(request, pk):
    school = get_object_or_404(School, pk=pk)
    context = {
        'dashboard_title': school.name,
        'school': school,
        'breadcrumb': [
            {"name": "Home", "url": '/'},
            {"name": "Schools", "url": '/schools/'},
            {"name": school.name, "url": '#'}
        ]
    }
    return render(request, 'schools/school_detail.html', context)


@login_required
@role_required(['school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def add_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            messages.success(request, f"School '{school.name}' added successfully!")
            return redirect('schools:school_list')
    else:
        form = SchoolForm()

    context = {
        'dashboard_title': "Add School",
        'form': form,
        'breadcrumb': [
            {"name": "Home", "url": '/'},
            {"name": "Schools", "url": '/schools/'},
            {"name": "Add School", "url": '#'}
        ]
    }
    return render(request, 'schools/add_school.html', context)


def login_school_admin(request):
    if request.user.is_authenticated:
        return redirect('schools:school_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('schools:school_list')
        else:
            messages.error(request, 'Invalid username or password.')

    context = {
        'dashboard_title': "School Admin Login",
    }
    return render(request, 'schools/login.html', context)


# -----------------------------
# DYNAMIC AJAX ENDPOINTS
# -----------------------------

@login_required
def load_subcounties(request):
    county_id = request.GET.get('county_id')
    subcounties = SubCounty.objects.filter(county_id=county_id).order_by("name")
    data = [{"id": sc.id, "name": sc.name} for sc in subcounties]
    return JsonResponse({"subcounties": data})


@login_required
def load_wards(request):
    subcounty_id = request.GET.get('subcounty_id')

    # Correct FK name: sub_county
    wards = Ward.objects.filter(sub_county_id=subcounty_id).order_by("name")

    data = [{"id": w.id, "name": w.name} for w in wards]
    return JsonResponse({"wards": data})
