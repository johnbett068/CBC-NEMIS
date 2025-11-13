from django.contrib import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school_level', 'county', 'sub_county', 'ward', 'address')
    search_fields = ('name', 'code', 'school_level')
    list_filter = ('school_level', 'county', 'sub_county')
    ordering = ('name',)
