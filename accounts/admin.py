from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Improved Admin UI for CustomUser:
    - Shows role
    - Shows profile image preview
    - Full search & filtering
    """

    # What to display in list page
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'profile_image_preview',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Add role + profile image to fieldsets
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),

        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'email')
        }),

        ("Permissions & Role", {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),

        ("Profile", {
            'fields': ('profile_image', 'profile_image_preview'),
        }),

        ("Important Dates", {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Add to "create user" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )

    readonly_fields = ('profile_image_preview', 'last_login', 'date_joined')

    # Method to show image preview
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; border-radius: 8px; object-fit: cover;" />',
                obj.profile_image.url
            )
        return "(No Image)"

    profile_image_preview.short_description = "Profile Preview"
