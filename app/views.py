# users/views.py

from rest_framework import viewsets, permissions
from .models import CustomUser, Customer, CustomerVerification, Auditor, Admin
from .serializers import (
    UserRegisterSerializer,
    UserListSerializer,
    CustomerSerializer,
    CustomerVerificationSerializer,
    AuditorSerializer,
    AdminSerializer
)
from .permissions import (
    IsCustomerOwner,
    IsAdminUser,
    IsAuditorUser,
    IsAuditorOwnerOrAdmin,
    IsAdminUserPermission
)


# ------------------------------
# 1️⃣ User ViewSet (Main Fix)
# ------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        # Allow registration for anyone
        if self.action == 'create':
            return [permissions.AllowAny()]
        # Allow viewing to authenticated users
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Updates/deletes restricted to admin or the same user
        else:
            return [permissions.IsAuthenticated(), IsAdminUserPermission()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserListSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # Registration: unauthenticated user
            return CustomUser.objects.none()

        # Admins can see all users
        if user.role == 'admin':
            return CustomUser.objects.all()

        # Normal users only see their own profile
        return CustomUser.objects.filter(id=user.id)


# ------------------------------
# 2️⃣ Customer ViewSet
# ------------------------------
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if hasattr(self.request.user, 'admin'):
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated(), IsCustomerOwner()]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin'):
            return Customer.objects.all()
        return Customer.objects.filter(user=user)


# ------------------------------
# 3️⃣ Customer Verification ViewSet
# ------------------------------
class CustomerVerificationViewSet(viewsets.ModelViewSet):
    queryset = CustomerVerification.objects.all()
    serializer_class = CustomerVerificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


# ------------------------------
# 4️⃣ Auditor ViewSet
# ------------------------------
class AuditorViewSet(viewsets.ModelViewSet):
    queryset = Auditor.objects.all()
    serializer_class = AuditorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuditorOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin'):
            return Auditor.objects.all()  # Admin sees all auditors
        elif hasattr(user, 'auditor'):
            return Auditor.objects.filter(user=user)  # Auditor sees self only
        return Auditor.objects.none()


# ------------------------------
# 5️⃣ Admin ViewSet
# ------------------------------
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserPermission]
