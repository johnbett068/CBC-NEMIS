from django.urls import path
from . import views

app_name = 'learners'

urlpatterns = [
    path('', views.learner_list, name='learner_list'),
    path('add/', views.add_learner, name='add_learner'),
    path('<int:pk>/', views.learner_detail, name='learner_detail'),
    path('<int:pk>/edit/', views.edit_learner, name='edit_learner'),
]
