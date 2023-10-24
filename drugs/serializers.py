from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Drug


class DrugCreateSerializer(serializers.Serializer):
    class Meta:
        model = Drug
        fields = "__all__"

    def create(self, validated_data):
        return Drug.objects.create(**validated_data)
