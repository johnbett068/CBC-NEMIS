from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher, SubjectAssignment, ClassAssignment
from subjects.models import Subject
from learners.models import Learner

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'username': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone', 'school', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'school': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }

    def __init__(self, *args, hide_school=False, **kwargs):
        super().__init__(*args, **kwargs)
        if hide_school and 'school' in self.fields:
            self.fields.pop('school')


class ClassAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['teacher', 'stream', 'year', 'is_class_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['teacher'].label_from_instance = (
            lambda obj: f"{obj.user.get_full_name()} ({obj.school.name})"
        )
        self.fields['stream'].label_from_instance = (
            lambda obj: f"{obj.grade} - {obj.name}"
        )

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border rounded px-3 py-2 w-full'
            })


class SubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubjectAssignment
        fields = ['teacher', 'subject', 'stream', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['teacher'].label_from_instance = (
            lambda obj: f"{obj.user.get_full_name()} ({obj.school.name})"
        )
        self.fields['subject'].label_from_instance = lambda obj: obj.name
        self.fields['stream'].label_from_instance = (
            lambda obj: f"{obj.grade} - {obj.name}"
        )

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border rounded px-3 py-2 w-full'
            })


class TeacherSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search Teacher',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email, or phone...',
            'class': 'border rounded px-3 py-2 w-full'
        })
    )


class LearnerForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        label="Learner Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'border rounded px-3 py-2 w-full'})
    )

    class Meta:
        model = Learner
        fields = [
            'birth_certificate_number', 'admission_number',
            'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'school', 'grade', 'year',
            'class_teacher', 'profile_image',
            'parent_full_name', 'parent_contact', 'relationship_to_learner',
            'county', 'sub_county', 'ward', 'postal_address', 'subjects'
        ]

        widgets = {
            'birth_certificate_number': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'admission_number': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'middle_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
            'gender': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'school': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'grade': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'year': forms.NumberInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'class_teacher': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'parent_full_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'parent_contact': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'relationship_to_learner': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'county': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'sub_county': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'ward': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'postal_address': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({
                    'class': 'border rounded px-3 py-2 w-full',
                })
