from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from accounts import views
# 이메일 인증을 위해 import함
# from rest_auth.registration.views import VerifyEmailView, RegisterView
# from rest_auth.views import (
#     LoginView, LogoutView, PasswordChangeView,
#     PasswordResetView, PasswordResetConfirmView
# )


urlpatterns = [
    path("signup/", views.AccountCreate.as_view(), name="signup"),
    path("api/token/", views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("profile_modification/", views.AccountAPI.as_view(), name="modification"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    # path("api/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
]

