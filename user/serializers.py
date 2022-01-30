from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, Profile


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone_number', 'role',
            'gender', 'address', 'password'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            gender=validated_data['gender'],
            address=validated_data['address'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone_number', 'role',
            'gender', 'address', 'last_login', 'date_joined',
            'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        read_only_fields = ('user',)
        fields = (
            'user', 'nick_name', 'date_of_birth', 'profile_picture', 'created_at'
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response
