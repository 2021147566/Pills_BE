from django.shortcuts import render
from django.http import HttpRequest
from rest_framework import status, permissions
from rest_framework.views import APIView
from accounts.serializers import (
    MyPageSerializer,
    ProfileSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from accounts.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes

# 새로운 사용자를 생성한 후에 이메일 확인 토큰을 생성하고 사용자 모델에 저장합니다. 이메일 인증 링크를 사용자의 이메일 주소로 전송합니다.
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

from accounts.tasks import test_task, send_verification_email
from rest_framework import views


class MyPageView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = MyPageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request, user_id):
        """사용자의 프로필을 받아 보여줍니다."""
        profile = get_object_or_404(User, id=user_id)
        if request.user.email == profile.email:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            if "present_pw" in request.data:  # 비밀번호 변경할 때
                # 현재 비밀번호가 일치하는지 확인.
                if check_password(request.data["present_pw"], user.password) == True:
                    # 새로 입력한 비밀번호와 비밀번호 확인이 일치하는지 확인.
                    if request.data["password"] == request.data["password_check"]:
                        serializer = UserSerializer(
                            user, data=request.data, partial=True
                        )
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response(
                                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {"message": "비밀번호가 일치하지 않습니다. 다시 입력하세요."},
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response(
                        {"message": "현재 비밀번호를 확인하세요."}, status=status.HTTP_403_FORBIDDEN
                    )

            else:  # 비밀번호는 변경하지 않을 때
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# class EmailVerificationView(APIView):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=uid)

#             if default_token_generator.check_token(user, token):
#                 # 사용자 모델의 email_verified 필드를 True로 설정
#                 # user.email_verified = True
#                 user.is_active = True
#                 user.save()
#                 return Response(
#                     {"message": "이메일 확인이 완료되었습니다."}, status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     {"message": "이메일 확인 링크가 잘못되었습니다."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
#             )


class AccountCreateView(APIView):
    print("APIVIEW시작!")

    def post(self, request):
        # 사용자 정보를 받아서 회원을 생성합니다.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message ": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"mssage": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    # serializer 의 토큰을 커스텀한 토큰키로 봐꿔준다
    # The serializer class that should be used for validating and deserializing input, and for serializing output
    serializer_class = CustomTokenObtainPairSerializer


# @permission_classes((permissions.AllowAny,))
# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSerializer


class Token_Test(APIView):
    def get(self, request):
        print(request.user)
        return Response("get요청")
