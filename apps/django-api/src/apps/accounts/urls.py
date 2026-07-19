from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from src.apps.accounts import views

urlpatterns = [
    # Authentication
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", views.logout, name="logout"),
    path("auth/change-password/", views.change_password, name="change_password"),
    # Profile
    path("profile/", views.UserDetailView.as_view(), name="user_detail"),
]
