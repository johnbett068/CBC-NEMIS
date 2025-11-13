from django.contrib import admin
from .models import Teacher, Stream, ClassAssignment, SubjectAssignment
from subjects.models import Subject

# --------------------------
# Safe Register for Subject only
# --------------------------
try:
    admin.site.register(Subject)
except admin.sites.AlreadyRegistered:
    pass

# --------------------------
# Inline Admins
# --------------------------
class ClassAssignmentInline(admin.TabularInline):
    model = ClassAssignment
    extra = 1
    autocomplete_fields = ['stream']
    fields = ['stream', 'year', 'is_class_teacher']
    ordering = ['year', 'stream__grade', 'stream__name']
    show_change_link = True

class SubjectAssignmentInline(admin.TabularInline):
    model = SubjectAssignment
    extra = 1
    autocomplete_fields = ['subject', 'stream']
    fields = ['subject', 'stream', 'year']
    ordering = ['year', 'stream__grade', 'subject__name']
    show_change_link = True

# --------------------------
# Teacher Admin
# --------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'role', 'school', 'phone', 'date_joined')
    list_filter = ('role', 'school')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'phone')
    ordering = ['school', 'role', 'user__last_name']
    inlines = [ClassAssignmentInline, SubjectAssignmentInline]
    autocomplete_fields = ['school', 'user']

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = "Teacher Name"

# --------------------------
# Stream Admin
# --------------------------
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('grade', 'name', 'school', 'school_level')
    list_filter = ('school', 'grade')
    search_fields = ('grade', 'name', 'school__name')
    ordering = ['school', 'grade', 'name']
    autocomplete_fields = ['school']
    list_per_page = 25

# --------------------------
# Class Assignment Admin
# --------------------------
@admin.register(ClassAssignment)
class ClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'stream', 'year', 'is_class_teacher')
    list_filter = ('year', 'is_class_teacher', 'stream__school', 'stream__grade')
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'stream__grade', 'stream__name')
    ordering = ['-year', 'stream__grade', 'stream__name']
    autocomplete_fields = ['teacher', 'stream']
    list_per_page = 30

    def teacher_name(self, obj):
        return obj.teacher.user.get_full_name() or obj.teacher.user.username
    teacher_name.short_description = "Teacher"

# --------------------------
# Subject Assignment Admin
# --------------------------
@admin.register(SubjectAssignment)
class SubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'subject', 'stream', 'year')
    list_filter = ('year', 'stream__school', 'stream__grade', 'subject__name')
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'subject__name', 'stream__grade')
    ordering = ['-year', 'stream__grade', 'subject__name']
    autocomplete_fields = ['teacher', 'subject', 'stream']
    list_per_page = 30

    def teacher_name(self, obj):
        return obj.teacher.user.get_full_name() or obj.teacher.user.username
    teacher_name.short_description = "Teacher"
