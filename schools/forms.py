from django import forms
from .models import School


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'code', 'sub_county', 'county', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'School Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'School Code'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subcounty'}),
            'county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'County'}),
            #'level': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Address'}),
            #'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            #'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        # Optional: Add Bootstrap classes to all fields dynamically
        for field in self.fields.values():
            if not 'class' in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'
