from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ---------------------------
# Custom User Manager
# ---------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# ---------------------------
# Custom User Model
# ---------------------------
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ---------------------------
# Admin Model
# ---------------------------
class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


# ---------------------------
# Auditor Model
# ---------------------------
class Auditor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auditor_id = models.CharField(max_length=20, unique=True)
    last_audit_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


# ---------------------------
# Customer Model
# ---------------------------
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    kyc_file = models.FileField(upload_to="kyc_files/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


# ---------------------------
# Customer Verification Model
# ---------------------------
class CustomerVerification(models.Model):
    STATUS_CHOICES = [
        ("approved", "Approved"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.user.email} - {self.status}"
