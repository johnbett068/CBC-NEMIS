from django.db import models
from schools.models import School  # Link each subject to its school (optional but useful)


class Subject(models.Model):
    """
    Represents a subject offered in the CBC curriculum.
    Subjects can optionally be linked to specific schools,
    supporting both local and national subject lists.
    """

    GRADE_CHOICES = [
        ('PrePrimary', 'Pre-Primary (PP1-PP2)'),
        ('LowerPrimary', 'Lower Primary (Grade 1-3)'),
        ('UpperPrimary', 'Upper Primary (Grade 4-6)'),
        ('JuniorSecondary', 'Junior Secondary (Grade 7-9)'),
        ('SeniorSecondary', 'Senior Secondary (Grade 10-12)'),
    ]

    name = models.CharField(max_length=100, unique=True)
    grade_level = models.CharField(max_length=20, choices=GRADE_CHOICES)
    is_compulsory = models.BooleanField(
        default=False,
        help_text="If true, this subject is automatically assigned to learners of this grade level."
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subjects',
        help_text="If null, the subject is considered a national curriculum subject."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['grade_level', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        unique_together = ('name', 'school')  # Prevent duplicates within the same school

    def __str__(self):
        school_name = self.school.name if self.school else "National"
        return f"{self.name} ({self.get_grade_level_display()}) - {school_name}"
