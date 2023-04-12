from rest_framework import serializers
from users.models import User
from django.db import transaction
from rest_framework.exceptions import ParseError


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk","username","email","password","profile_img","is_staff", "is_active",]

class ProfilePutSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username","profile_img"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk" ,"username","email" , "password","is_staff", "is_active",]

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email","username","password"]

class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","profile_img"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","email","username","introduce","profile_img"]

class SimpleJWTLoginSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","email","username","introduce","profile_img"]

    