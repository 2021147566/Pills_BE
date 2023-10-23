from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from accounts.models import User
# from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC


class AccountCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message ": "가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage" : f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    

class AccountAPI(APIView):
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
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class ProfileView(APIView):
    pass

# Email 인증을 위한 View입니다. 
# class ConfirmEmailView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, *args, **kwargs):
#         self.object = confirmation = self.get_object()
#         confirmation.confirm(self.request)
#         # A React Router Route will handle the failure scenario
#         return HttpResponseRedirect('/login/success/')

#     def get_object(self, queryset=None):
#         key = self.kwargs['key']
#         email_confirmation = EmailConfirmationHMAC.from_key(key)
#         if not email_confirmation:
#             if queryset is None:
#                 queryset = self.get_queryset()
#             try:
#                 email_confirmation = queryset.get(key=key.lower())
#             except EmailConfirmation.DoesNotExist:
#                 # A React Router Route will handle the failure scenario
#                 return HttpResponseRedirect('/login/failure/')
#         return email_confirmation

#     def get_queryset(self):
#         qs = EmailConfirmation.objects.all_valid()
#         qs = qs.select_related("email_address__user")
#         return qs