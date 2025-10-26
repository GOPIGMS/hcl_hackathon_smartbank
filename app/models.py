from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('auditor', 'Auditor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    kyc_file = models.FileField(upload_to='kyc_docs/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    account_status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_status}"


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    verified_count = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.user.username}"


class Auditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auditor_profile')
    auditor_id = models.CharField(max_length=50, unique=True)
    access_scope = models.CharField(max_length=50, default='limited')
    last_audit_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auditor: {self.user.username}"


class CustomerVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.user.username} - {self.status}"
