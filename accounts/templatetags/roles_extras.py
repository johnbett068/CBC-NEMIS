# accounts/templatetags/roles_extras.py
from django import template

register = template.Library()

@register.filter
def in_roles(role, roles_csv):
    """
    Usage in template:
      {% load roles_extras %}
      {% if user.is_authenticated and user.role|in_roles:"school_admin,teacher" %}
         ...
      {% endif %}
    Returns True if role is in the comma-separated roles_csv string.
    """
    if not role:
        return False
    if roles_csv is None:
        return False
    roles = [r.strip() for r in roles_csv.split(",") if r.strip()]
    return str(role).strip() in roles
