from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from accounts import views


urlpatterns = [
    path("signup/", views.AccountCreateView.as_view(), name="signup_view"),
    # path("login/", views.LoginView.as_view(), name="login_view"),
    # path(
    #     "verify-email/<str:uidb64>/<str:token>/",
    #     views.EmailVerificationView.as_view(),
    #     name="verify_email",
    # ),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path(
        "api/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path("<int:user_id>/mypage/", views.MyPageView.as_view(), name="my_page_view"),
    path("mocks/", views.Token_Test.as_view(), name="login_test"),
]
