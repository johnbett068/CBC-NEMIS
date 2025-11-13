from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    # Example URLs, adjust as needed
    path('', views.school_list, name='school_list'),
    path('<int:pk>/', views.school_detail, name='school_detail'),
]
