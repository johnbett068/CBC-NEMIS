from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    # -------------------------
    # Authentication URLs
    # -------------------------
    path('login/', views.login_teacher, name='login_teacher'),
    path('logout/', views.logout_teacher, name='logout_teacher'),

    # -------------------------
    # Dashboard / Home
    # -------------------------
    path('', views.home, name='home'),

    # -------------------------
    # Teacher Management
    # -------------------------
    path('list/', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_add, name='teacher_add'),
    path('<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('<int:pk>/', views.teacher_detail, name='teacher_detail'),

    # -------------------------
    # Class Assignments
    # -------------------------
    path('class-assignments/add/', views.class_assignment_add, name='class_assignment_add'),
    # (Optional future endpoint for listing all class assignments)
    # path('class-assignments/', views.class_assignment_list, name='class_assignment_list'),

    # -------------------------
    # Subject Assignments
    # -------------------------
    path('subject-assignments/', views.subject_assignment_list, name='subject_assignment_list'),
    path('subject-assignments/add/', views.subject_assignment_add, name='subject_assignment_add'),

    # -------------------------
    # Future-ready Endpoints (Phase 7+)
    # -------------------------
    # Teachers viewing their assigned learners
    # path('my-learners/', views.teacher_learners_list, name='teacher_learners_list'),

    # Class teacher view for managing all learners in their stream
    # path('class-teacher/learners/', views.class_teacher_learners, name='class_teacher_learners'),

    # For headteachers managing all teachers + streams
    # path('streams/manage/', views.stream_management, name='stream_management'),
]
