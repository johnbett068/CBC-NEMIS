from django.urls import path
from . import views

app_name = "location"

urlpatterns = [
    path("ajax/load-subcounties/", views.load_subcounties, name="ajax_load_subcounties"),
    path("ajax/load-wards/", views.load_wards, name="ajax_load_wards"),
]
