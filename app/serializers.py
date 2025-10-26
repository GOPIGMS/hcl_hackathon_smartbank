import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    CustomUser,
    Customer,
    CustomerVerification,
    Auditor,
    Admin,
)

# ---------------------------
# Utility for Base64 File Upload
# ---------------------------
class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


# ---------------------------
# User Registration Serializer
# ---------------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "password2", "first_name", "last_name", "phone"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ---------------------------
# User List Serializer
# ---------------------------
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "phone", "role", "created_at"]


# ---------------------------
# Customer Serializer
# ---------------------------
class CustomerSerializer(serializers.ModelSerializer):
    kyc_file = Base64FileField(required=False)

    class Meta:
        model = Customer
        fields = ["id", "user", "address", "phone", "kyc_file", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


# ---------------------------
# Customer Verification Serializer
# ---------------------------
class CustomerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerVerification
        fields = "__all__"
        read_only_fields = ["verified_at"]


# ---------------------------
# Auditor Serializer
# ---------------------------
class AuditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditor
        fields = ["id", "user", "auditor_id", "last_audit_date", "created_at"]
        read_only_fields = ["id", "created_at"]


# ---------------------------
# Admin Serializer
# ---------------------------
class AdminSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ["id", "user", "employee_id", "department", "last_activity", "created_at"]
        read_only_fields = ["id", "last_activity", "created_at"]
