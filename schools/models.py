from django.db import models
from location.models import County, SubCounty, Ward

class School(models.Model):
    SCHOOL_LEVEL_CHOICES = [
        ('PrePrimary', 'Pre-Primary'),
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # unique school code
    school_level = models.CharField(max_length=20, choices=SCHOOL_LEVEL_CHOICES)
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
