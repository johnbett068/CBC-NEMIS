from django import forms
from .models import School
from location.models import County, SubCounty, Ward


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'code', 'school_level', 'county', 'sub_county', 'ward', 'address']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'School Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'School Code'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Address'}),
            'school_level': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Counties always loaded
        self.fields['county'].queryset = County.objects.all().order_by('name')

        # Correct field name: sub_county NOT subcounty
        self.fields['sub_county'].queryset = SubCounty.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()

        # When form is submitted (POST)
        if self.is_bound:
            county_id = self.data.get('county')
            if county_id:
                self.fields['sub_county'].queryset = SubCounty.objects.filter(
                    county_id=county_id
                ).order_by('name')

            subcounty_id = self.data.get('sub_county')
            if subcounty_id:
                self.fields['ward'].queryset = Ward.objects.filter(
                    sub_county_id=subcounty_id
                ).order_by('name')

        else:
            # When editing an existing school
            if self.instance.pk:
                if self.instance.county:
                    self.fields['sub_county'].queryset = SubCounty.objects.filter(
                        county=self.instance.county
                    ).order_by('name')

                if self.instance.sub_county:
                    self.fields['ward'].queryset = Ward.objects.filter(
                        sub_county=self.instance.sub_county
                    ).order_by('name')

        # Add CSS classes
        self.fields['county'].widget.attrs['class'] = 'form-select'
        self.fields['sub_county'].widget.attrs['class'] = 'form-select'
        self.fields['ward'].widget.attrs['class'] = 'form-select'
