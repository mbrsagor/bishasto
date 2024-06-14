from rest_framework import views, status
from rest_framework.response import Response
from core.serializers.payment_serializer import CardInformationSerializer
import stripe


class PaymentAPI(views.APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}
        if serializer.is_valid():
            data_dict = serializer.data

            stripe.api_key = 'your-key-goes-here'
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status':
                status.HTTP_400_BAD_REQUEST
                        }
        return Response(response)


"""
{
  "object": "search_result",
  "url": "/v1/customers/search",
  "has_more": false,
  "data": [
    {
      "id": "cus_4QFJOjw2pOmAGJ",
      "object": "customer",
      "address": null,
      "balance": 0,
      "created": 1405641735,
      "currency": "usd",
      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",
      "delinquent": false,
      "description": "someone@example.com for Coderwall",
      "discount": null,
      "email": null,
      "invoice_prefix": "7D11B54",
      "invoice_settings": {
        "custom_fields": null,
        "default_payment_method": null,
        "footer": null,
        "rendering_options": null
      },
      "livemode": false,
      "metadata": {
        "foo": "bar"
      },
      "name": "fakename",
      "next_invoice_sequence": 25,
      "phone": null,
      "preferred_locales": [],
      "shipping": null,
      "tax_exempt": "none",
      "test_clock": null
    },
    {...},
    {...}
  ]
}
"""
