from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.generics import get_object_or_404


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname", "username", "email", "profile_img", "birthday",
                  "created_at", "updated_at")


class MyPageSerializer(serializers.ModelSerializer):
    drugs = serializers.SerializerMethodField()

    def get_drugs(self, obj):
        wishes = obj.drugs.all().order_by('-created_at')
        return DrugsSerializer(instance=drugs, many=True).data

    class Meta:
        model = User
        fields = ["drugs"]
