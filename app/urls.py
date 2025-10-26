from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CustomerViewSet,
    CustomerVerificationViewSet,
    AdminViewSet,
    AuditorViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"verifications", CustomerVerificationViewSet)
router.register(r"admins", AdminViewSet)
router.register(r"auditors", AuditorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
