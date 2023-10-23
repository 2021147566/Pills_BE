from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from accounts import views


urlpatterns = [
    path("signup/", views.AccountCreate.as_view(), name="signup_view"),
    path("login/", views.LoginView.as_view(),
         name="login_view"),
    path("profile_modification/", views.ProfileView.as_view(), name="modification"),
    path('verify-email/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='verify_email'),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    # path("api/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
]

