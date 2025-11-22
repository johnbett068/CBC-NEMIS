from django.http import JsonResponse
from django.shortcuts import render
from .models import County, SubCounty, Ward


def load_subcounties(request):
    """
    AJAX endpoint: return subcounties for a selected county.
    """
    county_id = request.GET.get("county_id")
    subcounties = SubCounty.objects.filter(county_id=county_id).order_by("name")

    data = [
        {"id": sub.id, "name": sub.name}
        for sub in subcounties
    ]

    return JsonResponse({"subcounties": data})


def load_wards(request):
    """
    AJAX endpoint: return wards for a selected subcounty.
    """
    subcounty_id = request.GET.get("subcounty_id")
    wards = Ward.objects.filter(sub_county_id=subcounty_id).order_by("name")

    data = [
        {"id": ward.id, "name": ward.name}
        for ward in wards
    ]

    return JsonResponse({"wards": data})
