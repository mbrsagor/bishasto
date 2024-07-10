import stripe
from rest_framework import views, status
from rest_framework.response import Response
from core.serializers.payment_serializer import CardInformationSerializer


class PaymentAPI(views.APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.data

            stripe.api_key = 'your-key-goes-here'
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status':
                status.HTTP_400_BAD_REQUEST
                        }
        return Response(response)
