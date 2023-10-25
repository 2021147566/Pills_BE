from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User


# Create your tests here.
class UserRegistrationAPITestCase(APITestCase):
    def testRegistation(self):
        url = reverse("signup_view")
        user_data = {
            "email": "dlg@daum.net",
            "username": "hyel",
            "nickname": "hyel",
            "password": "dlgpfl@1029",
        }
        response = self.client.post(url, user_data)
        print(f"회원가입 test : {response.data}")


class LoginTest(APITestCase):
    def setUp(self):
        self.data = {
            "email": "dlg@daum.net",
            "username": "hyel",
            "nickname": "hyel",
            "password": "dlgpfl@1029",
        }
        self.user = User.objects.create_user(
            email="dlg@daum.net",
            username="hyel",
            nickname="hyel",
            password="dlgpfl@1029",
        )  # create_user 가 아닌 create 을 쓰면 변수 전달 에러

    def test_login(self):
        print(self.user.password)
        print(self.user.is_active)
        # print(self.user.password)
        url = reverse("token_obtain_pair")
        user_data = {
            "email": "dlg@daum.net",
            "username": "hyel",
            "nickname": "hyel",
            "password": "dlgpfl@1029",
        }

        response = self.client.post(url, self.data)
        print(f"로그인 테스트 : {response.data}")


# class MyPageTest(APITestCase):
#     def setUp(self):
#         self.data = {
#             "email": "dlg@daum.net",
#             "username": "hyel",
#             "nickname": "hyel",
#             "password": "1029",
#         }
#         self.user = User.objects.create_user(
#             "dlg@daum.net", "hyel", "hyel", "1029"
#         )  # create_user 가 아닌 create 을 쓰면 변수 전달 에러

#     def test_mypage(self):
#         user = self.user
#         url = user.get_absolute_url()
#         access_token = self.client.post(reverse("signup_view"), self.data).data[
#             "access"
#         ]  # access 토큰 받아오기 - data['access'] 중요
#         response = self.client.get(
#             path=url,
#             HTTP_AUTHORIZATION=f"Bearer {access_token}",  # header 에 필요한 값 넣기
#         )
#         print(response)
#         return self.assertEqual(response.status_code, 200)
