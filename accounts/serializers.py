from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
)
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from drugs.serializers import DrugCreateSerializer
from django.contrib.auth.hashers import make_password
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.nickname = self.data.get("nickname")
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "nickname",
            "username",
            "email",
            "profile_img",
            "created_at",
            "updated_at",
        )


class MyPageSerializer(serializers.ModelSerializer):
    drugs = serializers.SerializerMethodField()

    def get_drugs(self, obj):
        drugs = obj.drugs.all().order_by("-created_at")
        return DrugCreateSerializer(instance=drugs, many=True).data

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "nickname",
            "email",
            "profile_img",
            "drugs",
        ]

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        token["nickname"] = user.nickname
        return token


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator])
    username = serializers.CharField(required=True, validators=[UniqueValidator])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "nickname",
            "email",
            "profile_img",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    # def validate_password(self, value: str) -> str:
    #     return make_password(value)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        # ...

        return token
