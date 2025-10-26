# users/admin.py
from django.contrib import admin
from .models import Customer, CustomerVerification, Admin, Auditor

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CustomerVerification)
class CustomerVerificationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'verified_by', 'status', 'verified_at']
    readonly_fields = ['verified_at']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'last_activity']

@admin.register(Auditor)
class AuditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'auditor_id', 'last_audit_date']

