from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role-based access control and optional profile images.
    """

    ROLE_CHOICES = [
        ('cabinet_secretary', 'Cabinet Secretary'),
        ('county_director', 'County Director'),
        ('subcounty_director', 'Subcounty Director'),
        ('school_admin', 'School Admin'),
        ('teacher', 'Teacher'),
        ('learner', 'Learner'),
    ]

    # Allow blank & null to avoid superuser creation errors and role issues
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        default='teacher'
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        # Safe fallback if role is missing
        role_display = self.get_role_display() if self.role else "No Role"
        return f"{self.username} ({role_display})"
