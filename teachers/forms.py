from django import forms
from django.contrib.auth.models import User
from .models import Teacher, SubjectAssignment, ClassAssignment, Stream
from subjects.models import Subject
from learners.models import Learner


# --------------------------
# User Form
# --------------------------
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': f'Enter {field.label}'
            })


# --------------------------
# Teacher Form
# --------------------------
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['role', 'phone', 'school', 'profile_image']

    def __init__(self, *args, hide_school=False, **kwargs):
        super().__init__(*args, **kwargs)
        if hide_school and 'school' in self.fields:
            self.fields.pop('school')

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': f'Enter {field.label}'
            })


# --------------------------
# Class Assignment Form
# --------------------------
class ClassAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['teacher', 'stream', 'year', 'is_class_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.school.name})"
        self.fields['stream'].label_from_instance = lambda obj: f"{obj.grade} - {obj.name}"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'border rounded px-3 py-2 w-full'})


# --------------------------
# Subject Assignment Form
# --------------------------
class SubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubjectAssignment
        fields = ['teacher', 'subject', 'stream', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.school.name})"
        self.fields['subject'].label_from_instance = lambda obj: obj.name
        self.fields['stream'].label_from_instance = lambda obj: f"{obj.grade} - {obj.name}"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'border rounded px-3 py-2 w-full'})


# --------------------------
# Teacher Search Form
# --------------------------
class TeacherSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search Teacher',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email, or phone...',
            'class': 'border rounded px-3 py-2 w-full'
        })
    )


# --------------------------
# Learner Form (Optional if used in teacher app)
# --------------------------
class LearnerForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        label="Learner Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Learner
        fields = [
            'birth_certificate_number', 'admission_number', 'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'school', 'grade', 'year', 'class_teacher',
            'profile_image', 'parent_full_name', 'parent_contact', 'relationship_to_learner',
            'county', 'sub_county', 'ward', 'postal_address', 'subjects'
        ]
        widgets = {
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({
                    'class': 'border rounded px-3 py-2 w-full',
                    'placeholder': f'Enter {field.label}'
                })
