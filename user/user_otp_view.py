from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User, ResetPhoneOTP
from user.serializers import PasswordSerializer


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


def send_reset_otp(phone):
    pass


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
