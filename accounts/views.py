from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import MyPageSerializer, ProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password


class MyPageView(APIView):
    def get(self, request, user_username):
        user = get_object_or_404(User, username=user_username)
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
            if 'present_pw' in request.data:  # 비밀번호 변경할 때
                # 현재 비밀번호가 일치하는지 확인.
                if check_password(request.data['present_pw'], user.password) == True:
                    # 새로 입력한 비밀번호와 비밀번호 확인이 일치하는지 확인.
                    if request.data['password'] == request.data['password_check']:
                        serializer = UserSerializer(
                            user, data=request.data, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"message": "비밀번호가 일치하지 않습니다. 다시 입력하세요."}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"message": "현재 비밀번호를 확인하세요."}, status=status.HTTP_403_FORBIDDEN)

            else:  # 비밀번호는 변경하지 않을 때
                serializer = UserSerializer(
                    user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
