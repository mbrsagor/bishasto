from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, Profile, PhoneNumberVerification


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


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'pk', 'old_password', 'new_password', 'confirm_password'
        ]

    def validate(self, attrs):
        """
        When user given new password & confirm password wrong the method will call.
        :param attrs: new password and confirm password
        :return: user_id
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Sorry! password not match'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        """
        When user input new password this method will save the password database.
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


# Phone number Verification serializer
class PhoneNumberVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumberVerification
        fields = '__all__'
