from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings  # Use AUTH_USER_MODEL instead of direct User import

from schools.models import School
from subjects.models import Subject


# --------------------------
# Stream (e.g. Grade 5 - Stream A)
# --------------------------
class Stream(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='streams')
    grade = models.CharField(max_length=20)
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('school', 'grade', 'name')
        ordering = ['grade', 'name']
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'

    def __str__(self):
        return f"{self.grade} - {self.name} ({self.school.name})"

    @property
    def school_level(self):
        g = self.grade.lower().strip()
        if 'pp' in g:
            return "Pre-Primary"
        elif any(str(n) in g for n in range(1, 4)):
            return "Lower Primary"
        elif any(str(n) in g for n in range(4, 7)):
            return "Upper Primary"
        elif any(str(n) in g for n in range(7, 10)):
            return "Junior Secondary"
        return "Senior Secondary"


# --------------------------
# Teacher Model
# --------------------------
class Teacher(models.Model):
    ROLE_CHOICES = [
        ('school_admin', 'School Admin'),
        ('head_teacher', 'Head Teacher'),
        ('class_teacher', 'Class Teacher'),
        ('subject_teacher', 'Subject Teacher'),
        ('support_staff', 'Support Staff'),
    ]

    # ✅ Use AUTH_USER_MODEL instead of direct User import
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    tsc_number = models.CharField(max_length=20, unique=True, help_text="Unique TSC number for teacher identification.")
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateField(default=date.today)
    profile_image = models.ImageField(
        upload_to='teacher_profiles/',
        blank=True,
        null=True,
        help_text="Optional profile image for the teacher."
    )

    class Meta:
        ordering = ['school', 'role', 'user__last_name']
        verbose_name = 'Teacher / Staff'
        verbose_name_plural = 'Teachers / Staff'

    def __str__(self):
        name = getattr(self.user, 'get_full_name', lambda: self.user.username)()
        return f"{name} - {self.get_role_display()} at {self.school.name}"

    # --- Role helpers ---
    @property
    def is_school_admin(self):
        return self.role == 'school_admin'

    @property
    def is_head_teacher(self):
        return self.role == 'head_teacher'

    @property
    def is_class_teacher(self):
        return self.role == 'class_teacher'

    @property
    def is_subject_teacher(self):
        return self.role == 'subject_teacher'

    @property
    def is_support_staff(self):
        return self.role == 'support_staff'

    # --- Related data ---
    @property
    def classes_managed(self):
        return self.class_assignments.filter(is_class_teacher=True).select_related('stream')

    @property
    def subjects_taught(self):
        return self.subject_assignments.select_related('subject', 'stream')

    def learners_taught(self):
        from learners.models import Learner
        stream_ids = self.subject_assignments.values_list('stream_id', flat=True)
        return Learner.objects.filter(stream_id__in=stream_ids)

    def learners_in_managed_classes(self):
        from learners.models import Learner
        stream_ids = self.class_assignments.filter(is_class_teacher=True).values_list('stream_id', flat=True)
        return Learner.objects.filter(stream_id__in=stream_ids)

    def subject_grade_pairs(self, year=None):
        qs = self.subject_assignments.all()
        if year:
            qs = qs.filter(year=year)
        return qs.values('subject__name', 'stream__grade', 'stream__name')


# --------------------------
# Class Assignment
# --------------------------
class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_assignments')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='class_assignments')
    year = models.IntegerField(default=date.today().year)
    is_class_teacher = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'stream', 'year')
        ordering = ['year', 'stream__grade', 'stream__name', 'teacher']
        verbose_name = 'Class Assignment'
        verbose_name_plural = 'Class Assignments'

    def __str__(self):
        role = "Class Teacher" if self.is_class_teacher else "Assigned Teacher"
        name = getattr(self.teacher.user, 'get_full_name', lambda: self.teacher.user.username)()
        return f"{name} - {role} for {self.stream.grade} {self.stream.name} ({self.year})"

    def clean(self):
        if self.is_class_teacher:
            if ClassAssignment.objects.filter(
                stream=self.stream, year=self.year, is_class_teacher=True
            ).exclude(pk=self.pk).exists():
                raise ValidationError(f"{self.stream} already has a class teacher for {self.year}.")


# --------------------------
# Subject Assignment
# --------------------------
class SubjectAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_assignments')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='subject_assignments')
    year = models.IntegerField(default=date.today().year)

    class Meta:
        unique_together = ('teacher', 'subject', 'stream', 'year')
        ordering = ['year', 'stream__grade', 'stream__name', 'subject__name']
        verbose_name = 'Subject Assignment'
        verbose_name_plural = 'Subject Assignments'

    def __str__(self):
        name = getattr(self.teacher.user, 'get_full_name', lambda: self.teacher.user.username)()
        return f"{name} - {self.subject.name} ({self.stream.grade} {self.stream.name}, {self.year})"
