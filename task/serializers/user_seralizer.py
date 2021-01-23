from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'auth_token'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        pass
