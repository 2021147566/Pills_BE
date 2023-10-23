from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from accounts.models import User
# 새로운 사용자를 생성한 후에 이메일 확인 토큰을 생성하고 사용자 모델에 저장합니다. 이메일 인증 링크를 사용자의 이메일 주소로 전송합니다.
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.utils.encoding import force_str
from .tasks import send_verification_email
from .tasks import test_task
from django.http import HttpRequest
from rest_framework import views
from django.contrib.auth.hashers import check_password


class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            print('EmailVerificationView실행 직전')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if default_token_generator.check_token(user, token):
                # 사용자 모델의 email_verified 필드를 True로 설정
                # user.email_verified = True
                user.is_active = True
                user.save()
                print('EmailVerificationView 실행')
                return Response({"message": "이메일 확인이 완료되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "이메일 확인 링크가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

class AccountCreate(APIView):
    def post(self, request):
        # 사용자 정보를 받아서 회원을 생성합니다.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 이메일 확인 토큰 생성
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('token과 uid부분')
            # 이메일에 확인 링크 포함하여 보내기
            verification_url = f"http://127.0.0.1:8000/accounts/verify-email/{uid}/{token}/"
            print(f'verification_url:{verification_url}')
            # 이메일 전송 코드 작성 및 이메일에 verification_url을 포함하여 보내기
            
            # 이메일 전송
            subject = '이메일 확인 링크'
            message = f'이메일 확인을 완료하려면 다음 링크를 클릭하세요: {verification_url}'
            from_email = 'tkdcks7@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            
            send_verification_email.delay(
                user.id, verification_url, user.email)
            print('send_verification_email 완료')

            return Response({"message ": "가입완료! 이메일 인증을 진행해주세요"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage" : f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message ": "회원정보 수정 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage" : f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer