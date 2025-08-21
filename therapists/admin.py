from django.contrib import admin
from .models import Therapist, Specialization, Certification, Schedule

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name_paternal', 'last_name_maternal', 'document_number', 'region', 'province', 'is_active']
    list_filter = ['is_active', 'gender', 'region', 'province']
    search_fields = ['first_name', 'last_name_paternal', 'last_name_maternal', 'document_number', 'email']
    list_editable = ['is_active']

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'therapist', 'issuing_organization', 'issue_date', 'expiry_date', 'is_active']
    list_filter = ['is_active', 'issue_date', 'expiry_date']
    search_fields = ['name', 'therapist__first_name', 'therapist__last_name_paternal', 'issuing_organization']
    list_editable = ['is_active']
    date_hierarchy = 'issue_date'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['therapist', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']
    search_fields = ['therapist__first_name', 'therapist__last_name_paternal']
    list_editable = ['is_available']
