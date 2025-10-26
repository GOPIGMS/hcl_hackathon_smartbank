from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Customer, CustomerVerification, Admin, Auditor
from .serializers import (
    UserSerializer, CustomerSerializer, CustomerVerificationSerializer,
    AdminSerializer, AuditorSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class CustomerVerificationViewSet(viewsets.ModelViewSet):
    queryset = CustomerVerification.objects.all()
    serializer_class = CustomerVerificationSerializer
    permission_classes = [IsAuthenticated]


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]


class AuditorViewSet(viewsets.ModelViewSet):
    queryset = Auditor.objects.all()
    serializer_class = AuditorSerializer
    permission_classes = [IsAuthenticated]
