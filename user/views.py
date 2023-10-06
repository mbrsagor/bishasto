from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import views, status, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken

from user import serializers
from .models import User, Profile
from utils import response, message, validation


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
            validation_error = validation.password_validation(request.data)
            if validation_error is not None:
                return Response(response.prepare_auth_failed(validation_error), status=status.HTTP_400_BAD_REQUEST)
            serializer = serializers.UserCreateSerializer(data=request.data)
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
            serializer = serializers.ProfileSerializer(queryset)
            return Response(response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            queryset = User.objects.get(id=self.request.user.id)
            serializer = serializers.UserSerializer(queryset)
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
                serializer = serializers.ProfileSerializer(profile, data=request.data)
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
    serializer_class = serializers.PasswordChangeSerializer


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
        return Response(response.prepare_success_response(message.USER_LOGOUT), status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    list:
    Return a list of all the existing users.
    read:
    Return the given user.
    me:
    Return authenticated user.
    """
    queryset = User.objects.all()
    serializer_class = PasswordSerializer

    # permission_classes = (IsSuperuserOrIsSelf,)

    # @action(detail=True, methods=['put'])
    def post(self, request):
        phone = request.data.get('phone', False)
        # new_password = request.data.get('new_password')
        if phone:
            old = ResetPhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.last()
                validated = old.validated

                if validated:

                    serializer = PasswordSerializer(data=request.data)

                    if serializer.is_valid():
                        user.set_password(serializer.data.get('new_password'))
                        user.save()
                        return Response({'status': 'password set'}, status=status.HTTP_200_OK)
                    return Response({'status': 'password not2 set'})
                return Response({'status': 'password not3 set'})
        return Response({'status': 'password not 4set'})


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            key = send_reset_otp(phone)
            old = User.objects.filter(phone=phone)
            if old.exists():
                # old  = old.first()
                # count = old.count
                # old.count = count + 1
                # old.save()
                ResetPhoneOTP.objects.create(
                    # name = name,
                    phone=phone,
                    otp=key

                )
                # print('Count Increase', count)

                # print(key)
                return Response({
                    'status': True,
                    'detail': 'OTP sent successfully.'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone Number DoesNotExist'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Phone Number is not given in body.'
            })


class ValidateResetOTP(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = ResetPhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.last()
                otp = old.otp
                # old = Customer.objects.filter(otp)
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP mactched. Please proceed for Reset Password.'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect.'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request.'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validations'
            })
