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

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
