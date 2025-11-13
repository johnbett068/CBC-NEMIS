from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.subject_add, name='subject_add'),
]
