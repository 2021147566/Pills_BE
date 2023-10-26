from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include, re_path
from accounts import views


urlpatterns = [
    path("signup/", views.AccountCreateView.as_view(), name="signup_view"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),  # 로그인
    # path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "register/",
        views.CustomRegisterView.as_view(),  # 회원가입
        name="register",
    ),
    # 유효한 이메일이 유저에게 전달
    re_path(
        r"^account-confirm-email/$",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        views.ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
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
