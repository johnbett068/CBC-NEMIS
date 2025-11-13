from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('cs/', views.cs_dashboard, name='cs_dashboard'),
    path('county/', views.county_dashboard, name='county_dashboard'),
    path('subcounty/', views.subcounty_dashboard, name='subcounty_dashboard'),
    path('school-admin/', views.school_admin_dashboard, name='school_admin_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
