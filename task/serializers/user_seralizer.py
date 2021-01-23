from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
            'is_staff', 'is_superuser', 'last_login'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        pass
