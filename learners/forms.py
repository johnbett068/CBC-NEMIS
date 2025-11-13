from django import forms
from .models import Learner


class LearnerForm(forms.ModelForm):
    # Map the optional profile image to model's profile_image
    profile_image = forms.ImageField(
        required=False,
        label="Learner Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Learner
        fields = [
            'birth_certificate_number',
            'admission_number',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'school',
            'grade',
            'year',
            'class_teacher',
            'parent_full_name',
            'parent_contact',
            'relationship_to_learner',
            'county',
            'sub_county',
            'ward',
            'postal_address',
            'subjects',
            'profile_image',  # updated field
        ]
        widgets = {
            'birth_certificate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'}),
            'parent_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship_to_learner': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'sub_county': forms.Select(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-control'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Only image files are allowed.")
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB ).")
        return image
