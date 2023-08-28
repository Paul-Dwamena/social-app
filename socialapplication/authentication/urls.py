from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter






urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', RegisterView.as_view(), name="register"),
    path('auth/update-profile', UpdateProfileView.as_view(), name="update_profile"),
    path('auth/get-profile-details', GetProfileView.as_view(), name="get_profile"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
