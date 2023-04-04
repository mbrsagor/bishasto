from django.contrib.auth import logout
from rest_framework import views, status, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from utils import message
from .models import User, Profile
from .serializers import UserCreateSerializer, UserSerializer, ProfileSerializer, PasswordChangeSerializer
from utils import response
from utils.validation import password_validation


# User Registration API
class UserCreateAPIView(views.APIView):
    """
    Name: user registration API View
    URL: /api/v1/user/registration/
    Method: POST
    """
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        try:
            validation_error = password_validation(request.data)
            if validation_error is not None:
                return Response(response.prepare_auth_failed(validation_error), status=status.HTTP_400_BAD_REQUEST)
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(response.prepare_create_success_auth(message.USER_CREATED),
                                status=status.HTTP_201_CREATED)
            else:
                return Response(response.prepare_auth_failed(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(response.prepare_auth_failed(str(ex)), status=status.HTTP_200_OK)


# User Login API
class LoginAPIView(ObtainAuthToken):
    """
    Name: Signout API view
    URL: /api/v1/user/login/
    Method: POST
    """
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
        user = serializer.validated_data['user']
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'message': message.USER_LOGIN
        }, status=status.HTTP_200_OK)


# User Profile API
class ProfileAPIView(views.APIView):
    """
    Name: User profile view
    URL: /api/v1/user/profile/
    Method: GET
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        try:
            queryset = Profile.objects.get(id=self.request.user.id)
            serializer = ProfileSerializer(queryset)
            return Response(response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            queryset = User.objects.get(id=self.request.user.id)
            serializer = UserSerializer(queryset)
            return Response(response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)


# Profile update
class ProfileUpdateView(views.APIView):
    """
    Name: user profile update
    URL:/api/v1/user/profile/<pk>/
    Method: PUT
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return None

    def put(self, request, pk):
        try:
            profile = self.get_object(pk)
            if profile is not None:
                serializer = ProfileSerializer(profile, data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(response.prepare_create_success_response(serializer.data),
                                    status=status.HTTP_201_CREATED)
                return Response(response.prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response.prepare_error_response(message.NOTFOUND), status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(response.prepare_auth_failed(str(ex)), status=status.HTTP_200_OK)


# Change Password
class ChangePasswordView(generics.UpdateAPIView):
    """
    Name: Password change view
    URL: /api/v1/user/password-change/<pk>/
    Method: PUT
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer


# Logout
class LogoutView(views.APIView):
    """
    Name: Logout view
    URL:/api/user/logout/
    Method: POST
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        logout(request)
        return Response(response.prepare_success_response('user has been logout'), status=status.HTTP_200_OK)
