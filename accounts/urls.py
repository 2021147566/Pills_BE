from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from accounts import views


urlpatterns = [
    # path("signup/", views.AccountCreate.as_view(), name="signup"),
    # path("login/", views.AccountLogin.as_view(), name="login"),
    # path("logout/", views.AccountLogout.as_view(), name="logout"),
    # path("mock/", views.MockView.as_view(), name="test"),
    # path("api/token/", views.CustomTokenObtainPairView.as_view(),
    #      name="token_obtain_pair"),
    # path("api/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path('<str:user_username>/mypage/',
         views.MyPageView.as_view(), name='my_page_view'),

]
# 호오~bb
