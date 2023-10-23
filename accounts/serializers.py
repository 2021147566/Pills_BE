from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs[self.username_field])

        if check_password(attrs['password'], user.password) == False:
            raise NotFound("사용자를 찾을 수 없습니다. 로그인 정보를 확인하세요.") # 404 Not Found
        elif user.is_active == False:
            raise AuthenticationFailed("이메일 인증이 필요합니다.") # 401 Unauthorized
        else:
            # 기본 동작을 실행하고 반환된 데이터를 저장합니다.
            data = super().validate(attrs)
            return data
    
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['nickname'] = user.nickname
        return token
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'nickname',
            'birthday',
            'password'
        ]
        

    def create(self, validated_data):   
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance