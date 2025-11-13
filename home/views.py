from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

from teachers.models import Teacher, ClassAssignment, SubjectAssignment
from learners.models import Learner
from schools.models import School

# Import role-checking helpers (you’ll create these in users/utils.py)
from users.utils import (
    is_cabinet_secretary,
    is_county_director,
    is_subcounty_director,
    is_school_admin,
    is_teacher,
)

# --------------------------
# Home / Main Dashboard View
# --------------------------
@login_required
def home(request):
    """
    Home page showing quick stats and role cards.
    Users navigate to their specific dashboards via role cards.
    """
    user = request.user
    context = {}

    # Default statistics (visible to all roles)
    context['total_schools'] = School.objects.count()
    context['total_teachers'] = Teacher.objects.count()
    context['total_learners'] = Learner.objects.count()

    # Get user role
    role = getattr(user, 'role', None)
    context['role'] = role

    # Role cards (each role gets specific dashboard access)
    role_cards = {
        "Cabinet Secretary": {
            "color": "blue",
            "icon": "fa-university",
            "description": "Access national reports, analytics, and manage all education levels.",
            "url": reverse_lazy('home:cs_dashboard') if is_cabinet_secretary(user) else "#"
        },
        "County Director": {
            "color": "green",
            "icon": "fa-map-marked-alt",
            "description": "Manage and review county-level school performance and teacher distribution.",
            "url": reverse_lazy('home:county_dashboard') if is_county_director(user) else "#"
        },
        "Subcounty Director": {
            "color": "yellow",
            "icon": "fa-city",
            "description": "Oversee schools within sub-counties and coordinate reports from school heads.",
            "url": reverse_lazy('home:subcounty_dashboard') if is_subcounty_director(user) else "#"
        },
        "School Admin": {
            "color": "indigo",
            "icon": "fa-school",
            "description": "Manage teachers, learners, and school operations efficiently.",
            "url": reverse_lazy('home:school_admin_dashboard') if is_school_admin(user) else "#"
        },
        "Teacher": {
            "color": "purple",
            "icon": "fa-chalkboard-teacher",
            "description": "View class lists, enter assessments, and collaborate with other teachers.",
            "url": reverse_lazy('home:teacher_dashboard') if is_teacher(user) else "#"
        },
        "Learner": {
            "color": "pink",
            "icon": "fa-user-graduate",
            "description": "Track progress, performance, and upcoming assessments.",
            "url": "#"  # Learner dashboard not ready yet
        },
    }

    context['role_cards'] = role_cards
    context['roles'] = list(role_cards.keys())
    context['breadcrumb'] = [
        {"name": "Home", "url": reverse('home:home')}
    ]

    return render(request, 'home/home.html', context)


# --------------------------
# Individual Dashboard Views
# --------------------------

@login_required
@user_passes_test(is_cabinet_secretary)
def cs_dashboard(request):
    context = {
        'dashboard_title': "Cabinet Secretary Dashboard",
        'schools': School.objects.all(),
        'teachers': Teacher.objects.all(),
        'learners': Learner.objects.all(),
        'breadcrumb': [
            {"name": "Home", "url": reverse('home:home')},
            {"name": "Cabinet Secretary Dashboard", "url": reverse('home:cs_dashboard')}
        ]
    }
    return render(request, 'home/cs_dashboard.html', context)


@login_required
@user_passes_test(is_county_director)
def county_dashboard(request):
    user = request.user
    county = getattr(user, 'county', None)
    context = {
        'dashboard_title': "County Director Dashboard",
        'schools': School.objects.filter(county=county) if county else School.objects.none(),
        'teachers': Teacher.objects.filter(school__county=county) if county else Teacher.objects.none(),
        'learners': Learner.objects.filter(school__county=county) if county else Learner.objects.none(),
        'breadcrumb': [
            {"name": "Home", "url": reverse('home:home')},
            {"name": "County Director Dashboard", "url": reverse('home:county_dashboard')}
        ]
    }
    return render(request, 'home/county_dashboard.html', context)


@login_required
@user_passes_test(is_subcounty_director)
def subcounty_dashboard(request):
    user = request.user
    subcounty = getattr(user, 'subcounty', None)
    context = {
        'dashboard_title': "Subcounty Director Dashboard",
        'schools': School.objects.filter(subcounty=subcounty) if subcounty else School.objects.none(),
        'teachers': Teacher.objects.filter(school__subcounty=subcounty) if subcounty else Teacher.objects.none(),
        'learners': Learner.objects.filter(school__subcounty=subcounty) if subcounty else Learner.objects.none(),
        'breadcrumb': [
            {"name": "Home", "url": reverse('home:home')},
            {"name": "Subcounty Director Dashboard", "url": reverse('home:subcounty_dashboard')}
        ]
    }
    return render(request, 'home/subcounty_dashboard.html', context)


@login_required
@user_passes_test(is_school_admin)
def school_admin_dashboard(request):
    user = request.user
    school = getattr(user, 'school', None)
    teachers = Teacher.objects.filter(school=school) if school else Teacher.objects.none()
    learners = Learner.objects.filter(school=school) if school else Learner.objects.none()

    context = {
        'dashboard_title': "School Admin Dashboard",
        'school': school,
        'teachers': teachers,
        'learners': learners,
        'total_teachers': teachers.count(),
        'total_learners': learners.count(),
        'breadcrumb': [
            {"name": "Home", "url": reverse('home:home')},
            {"name": "School Admin Dashboard", "url": reverse('home:school_admin_dashboard')}
        ]
    }
    return render(request, 'home/school_admin_dashboard.html', context)


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    user = request.user
    teacher_profile = getattr(user, 'teacher_profile', None)

    if teacher_profile:
        classes = ClassAssignment.objects.filter(teacher=teacher_profile)
        subjects = SubjectAssignment.objects.filter(teacher=teacher_profile)
        learners = Learner.objects.filter(school=teacher_profile.school)
        context = {
            'dashboard_title': "Teacher Dashboard",
            'school': teacher_profile.school,
            'classes': classes,
            'subjects': subjects,
            'learners': learners,
            'total_classes': classes.count(),
            'total_subjects': subjects.count(),
            'total_learners': learners.count(),
            'breadcrumb': [
                {"name": "Home", "url": reverse('home:home')},
                {"name": "Teacher Dashboard", "url": reverse('home:teacher_dashboard')}
            ]
        }
    else:
        context = {
            'dashboard_title': "Teacher Dashboard",
            'classes': [],
            'subjects': [],
            'learners': [],
            'total_classes': 0,
            'total_subjects': 0,
            'total_learners': 0,
            'breadcrumb': [
                {"name": "Home", "url": reverse('home:home')},
                {"name": "Teacher Dashboard", "url": reverse('home:teacher_dashboard')}
            ]
        }

    return render(request, 'home/teacher_dashboard.html', context)
