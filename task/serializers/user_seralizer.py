import datetime
from account.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.utils import datetime_to_epoch

SUPERUSER_LIFETIME = datetime.timedelta(minutes=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
            'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups'
        )


class TokenObtainTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainTokenSerializer, cls).get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        if user:
            token.payload['exp'] = datetime_to_epoch(token.current_time + SUPERUSER_LIFETIME)
            return token
