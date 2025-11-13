from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='subcounties')

    class Meta:
        unique_together = ('name', 'county')

    def __str__(self):
        return f"{self.name}, {self.county.name}"
        

class Ward(models.Model):
    name = models.CharField(max_length=100)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name='wards')

    class Meta:
        unique_together = ('name', 'sub_county')

    def __str__(self):
        return f"{self.name}, {self.sub_county.name}"
