from django.db import models
from datetime import date

from schools.models import School
from location.models import County, SubCounty, Ward


class Learner(models.Model):
    GRADE_CHOICES = [
        ('PP1', 'PP1'), ('PP2', 'PP2'),
        ('Grade 1', 'Grade 1'), ('Grade 2', 'Grade 2'), ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'), ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'), ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'), ('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    RELATIONSHIP_CHOICES = [
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Guardian', 'Guardian'),
        ('Other', 'Other'),
    ]

    # Core identification
    birth_certificate_number = models.CharField(
        max_length=50, primary_key=True, unique=True
    )
    admission_number = models.CharField(max_length=20, unique=True)

    # Basic info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # School details
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    year = models.IntegerField(default=date.today().year)
    admission_date = models.DateField(default=date.today)

    class_teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_learners'
    )

    # Profile
    profile_image = models.ImageField(
        upload_to='learner_profiles/',
        blank=True,
        null=True,
        help_text="Optional profile image for the learner."
    )

    # Parent/guardian info
    parent_full_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=15)
    relationship_to_learner = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)

    # Location info
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    postal_address = models.CharField(max_length=100, help_text="e.g. P.O. Box 36 Bomet")

    # Academic subjects
    subjects = models.ManyToManyField(
        'subjects.Subject',
        related_name='learners',
        blank=True,
        help_text="Compulsory subjects are auto-assigned; optional subjects can be selected here"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.grade})"

    class Meta:
        ordering = ['school', 'grade', 'last_name', 'first_name']
        verbose_name = "Learner"
        verbose_name_plural = "Learners"
