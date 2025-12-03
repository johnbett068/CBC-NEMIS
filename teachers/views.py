# teachers/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser as User

from .models import Teacher, ClassAssignment, SubjectAssignment
from learners.models import Learner

from .forms import (
    UserForm,
    TeacherForm,
    ClassAssignmentForm,
    SubjectAssignmentForm,
    TeacherSearchForm
)

from utils.decorators import role_required
from accounts.views import redirect_user_by_role


# ============================================================
# TEACHER HOME / DASHBOARD
# ============================================================
@login_required
@role_required(['teacher', 'school_admin', 'head_teacher',
                'subcounty_director', 'county_director', 'cabinet_secretary'])
def home(request):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    total_teachers = Teacher.objects.filter(school=school).count() if school else Teacher.objects.count()
    total_learners = Learner.objects.filter(school=school).count() if school else Learner.objects.count()
    total_schools = 1 if school else Teacher.objects.values('school').distinct().count()

    context = {
        'dashboard_title': "Teacher Dashboard",
        'total_teachers': total_teachers,
        'total_learners': total_learners,
        'total_schools': total_schools,
        'school': school,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teacher Dashboard", "url": '#'}
        ]
    }
    return render(request, 'teachers/home.html', context)


# ============================================================
# LIST TEACHERS
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
def teacher_list(request):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    teachers = Teacher.objects.filter(school=school).order_by('role', 'user__last_name')

    search_form = TeacherSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        q = search_form.cleaned_data['query']
        teachers = teachers.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__email__icontains=q) |
            Q(phone__icontains=q)
        )

    context = {
        'dashboard_title': "Teachers",
        'teachers': teachers,
        'search_form': search_form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teachers", "url": '#'}
        ]
    }
    return render(request, 'teachers/teacher_list.html', context)


# ============================================================
# TEACHER DETAIL
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
def teacher_detail(request, pk):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    teacher = get_object_or_404(Teacher, pk=pk, school=school)

    context = {
        'dashboard_title': f"{teacher.user.get_full_name()}",
        'teacher': teacher,
        'class_assignments': teacher.class_assignments.all(),
        'subject_assignments': teacher.subject_assignments.select_related('subject'),
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teachers", "url": reverse_lazy('teachers:teacher_list')},
            {"name": teacher.user.get_full_name(), "url": '#'}
        ]
    }
    return render(request, 'teachers/teacher_detail.html', context)


# ============================================================
# ADD TEACHER
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
@transaction.atomic
def teacher_add(request):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST, request.FILES, hide_school=True)

        if user_form.is_valid() and teacher_form.is_valid():

            # Create user (CustomUser)
            user = user_form.save(commit=False)
            password = User.objects.make_random_password(8)
            user.set_password(password)
            user.save()

            # Create teacher profile
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.school = school
            teacher.save()

            # Attempt to send email (non-blocking)
            try:
                from django.core.mail import send_mail
                send_mail(
                    subject="Your Teacher Account",
                    message=f"Hello {user.get_full_name()}\nUsername: {user.username}\nPassword: {password}",
                    from_email="no-reply@myschool.com",
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                messages.warning(request, "Teacher added but email failed to send.")

            messages.success(request, "Teacher added successfully.")
            return redirect('teachers:teacher_list')
        else:
            # Show form errors
            messages.error(request, "Please fix the errors below.")
    else:
        user_form = UserForm()
        teacher_form = TeacherForm(hide_school=True)

    return render(request, 'teachers/teacher_form.html', {
        'dashboard_title': "Add Teacher",
        'user_form': user_form,
        'teacher_form': teacher_form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teachers", "url": reverse_lazy('teachers:teacher_list')},
            {"name": "Add Teacher", "url": '#'}
        ]
    })


# ============================================================
# UPDATE TEACHER
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
@transaction.atomic
def teacher_update(request, pk):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    teacher = get_object_or_404(Teacher, pk=pk, school=school)
    user = teacher.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        teacher_form = TeacherForm(request.POST, request.FILES, instance=teacher, hide_school=True)

        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            messages.success(request, "Teacher updated successfully.")
            return redirect('teachers:teacher_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        user_form = UserForm(instance=user)
        teacher_form = TeacherForm(instance=teacher, hide_school=True)

    return render(request, 'teachers/teacher_form.html', {
        'dashboard_title': f"Update {teacher.user.get_full_name()}",
        'user_form': user_form,
        'teacher_form': teacher_form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teachers", "url": reverse_lazy('teachers:teacher_list')},
            {"name": f"Update {teacher.user.get_full_name()}", "url": '#'}
        ]
    })


# ============================================================
# DELETE TEACHER
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
@transaction.atomic
def teacher_delete(request, pk):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    teacher = get_object_or_404(Teacher, pk=pk, school=school)

    if request.method == 'POST':
        user = teacher.user
        teacher.delete()
        user.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect('teachers:teacher_list')

    return render(request, 'teachers/teacher_confirm_delete.html', {
        'dashboard_title': f"Delete {teacher.user.get_full_name()}",
        'teacher': teacher,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Teachers", "url": reverse_lazy('teachers:teacher_list')},
            {"name": f"Delete {teacher.user.get_full_name()}", "url": '#'}
        ]
    })


# ============================================================
# CLASS ASSIGNMENT
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
def class_assignment_add(request):
    if request.method == 'POST':
        form = ClassAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class assignment added successfully.")
            return redirect('teachers:teacher_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ClassAssignmentForm()

    return render(request, 'teachers/class_assignment_form.html', {
        'dashboard_title': "Add Class Assignment",
        'form': form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Class Assignments", "url": '#'}
        ]
    })


# ============================================================
# SUBJECT ASSIGNMENTS
# ============================================================
@login_required
@role_required(['school_admin', 'head_teacher'])
def subject_assignment_list(request):
    teacher_profile = getattr(request.user, 'teacher_profile', None)
    school = getattr(teacher_profile, 'school', None)

    assignments = SubjectAssignment.objects.filter(
        teacher__school=school
    ).select_related('teacher', 'subject').order_by('stream__grade', 'subject__name')

    return render(request, 'teachers/subject_assignment_list.html', {
        'dashboard_title': "Subject Assignments",
        'assignments': assignments,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Subject Assignments", "url": '#'}
        ]
    })


@login_required
@role_required(['school_admin', 'head_teacher'])
def subject_assignment_add(request):
    if request.method == 'POST':
        form = SubjectAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject assignment added successfully.")
            return redirect('teachers:subject_assignment_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SubjectAssignmentForm()

    return render(request, 'teachers/subject_assignment_form.html', {
        'dashboard_title': "Add Subject Assignment",
        'form': form,
        'breadcrumb': [
            {"name": "Home", "url": reverse_lazy('home:home')},
            {"name": "Subject Assignments", "url": reverse_lazy('teachers:subject_assignment_list')},
            {"name": "Add", "url": '#'}
        ]
    })


# ============================================================
# LOGIN WITH redirect_user_by_role
# ============================================================
def login_teacher(request):
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'teachers/login.html', {
        'dashboard_title': "Teacher Login"
    })


def logout_teacher(request):
    logout(request)
    return redirect("teachers:login_teacher")
