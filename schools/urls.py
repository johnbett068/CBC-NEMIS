from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('', views.school_list, name='school_list'),
    path('<int:pk>/', views.school_detail, name='school_detail'),

    # ADD SCHOOL URL (missing)
    path('add/', views.add_school, name='add_school'),

    # OPTIONAL: school admin login (if you want it here)
    path('login/', views.login_school_admin, name='school_login'),

    path('ajax/subcounties/', views.load_subcounties, name='ajax_load_subcounties'),
    path('ajax/wards/', views.load_wards, name='ajax_load_wards'),
]
