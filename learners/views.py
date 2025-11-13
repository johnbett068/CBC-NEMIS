from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Learner
from .forms import LearnerForm
from utils.decorators import role_required


# --------------------------
# List Learners
# --------------------------
@login_required
@role_required(['teacher', 'school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def learner_list(request):
    """
    List all learners.
    School-level users see learners in their school only.
    Higher-level users see all learners.
    """
    user_profile = getattr(request.user, 'teacher_profile', None)
    school_admin_profile = getattr(request.user, 'school_admin_profile', None)

    if user_profile:
        school = user_profile.school
        learners = Learner.objects.filter(school=school).order_by('grade', 'last_name', 'first_name')
    elif school_admin_profile:
        school = school_admin_profile.school
        learners = Learner.objects.filter(school=school).order_by('grade', 'last_name', 'first_name')
    else:
        learners = Learner.objects.all().order_by('school', 'grade', 'last_name', 'first_name')

    context = {
        'dashboard_title': "Learners",
        'learners': learners,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Learners", "url": '#'}
        ]
    }
    return render(request, 'learners/learner_list.html', context)


# --------------------------
# Learner Detail
# --------------------------
@login_required
@role_required(['teacher', 'school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def learner_detail(request, pk):
    """
    Show detailed info for a single learner.
    Restrict access for school-level users.
    """
    learner = get_object_or_404(Learner, pk=pk)

    # School-level access check
    user_profile = getattr(request.user, 'teacher_profile', None)
    school_admin_profile = getattr(request.user, 'school_admin_profile', None)
    user_school = getattr(user_profile or school_admin_profile, 'school', None)
    if user_school and learner.school != user_school:
        return redirect('learners:learner_list')

    context = {
        'dashboard_title': f"Learner: {learner.first_name} {learner.last_name}",
        'learner': learner,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Learners", "url": reverse_lazy('learners:learner_list')},
            {"name": f"{learner.first_name} {learner.last_name}", "url": '#'}
        ]
    }
    return render(request, 'learners/learner_detail.html', context)


# --------------------------
# Add Learner
# --------------------------
@login_required
@role_required(['teacher', 'school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def add_learner(request):
    """
    Add a new learner.
    School-level users auto-assign learners to their school.
    """
    user_profile = getattr(request.user, 'teacher_profile', None)
    school_admin_profile = getattr(request.user, 'school_admin_profile', None)

    if request.method == 'POST':
        form = LearnerForm(request.POST, request.FILES)
        if form.is_valid():
            learner = form.save(commit=False)
            if user_profile:
                learner.school = user_profile.school
            elif school_admin_profile:
                learner.school = school_admin_profile.school
            learner.save()
            return redirect('learners:learner_list')
    else:
        form = LearnerForm()

    context = {
        'dashboard_title': "Add Learner",
        'form': form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Learners", "url": reverse_lazy('learners:learner_list')},
            {"name": "Add Learner", "url": '#'}
        ]
    }
    return render(request, 'learners/add_learner.html', context)


# --------------------------
# Edit Learner
# --------------------------
@login_required
@role_required(['teacher', 'school_admin', 'subcounty_director', 'county_director', 'cabinet_secretary'])
def edit_learner(request, pk):
    """
    Edit an existing learner.
    Restrict access for school-level users.
    """
    learner = get_object_or_404(Learner, pk=pk)

    user_profile = getattr(request.user, 'teacher_profile', None)
    school_admin_profile = getattr(request.user, 'school_admin_profile', None)
    user_school = getattr(user_profile or school_admin_profile, 'school', None)
    if user_school and learner.school != user_school:
        return redirect('learners:learner_list')

    if request.method == 'POST':
        form = LearnerForm(request.POST, request.FILES, instance=learner)
        if form.is_valid():
            form.save()
            return redirect('learners:learner_list')
    else:
        form = LearnerForm(instance=learner)

    context = {
        'dashboard_title': f"Edit Learner: {learner.first_name} {learner.last_name}",
        'form': form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Learners", "url": reverse_lazy('learners:learner_list')},
            {"name": f"Edit {learner.first_name} {learner.last_name}", "url": '#'}
        ]
    }
    return render(request, 'learners/add_learner.html', context)
