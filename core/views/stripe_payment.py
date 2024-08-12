import stripe
from django.conf import settings
from django.views import generic, View

from .models import Ticket
stripe.api_key = settings.STRIPE_SECRET_KEY

# Stripe payment 
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://localhost:8000"  # Change this to your actual domain
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Buy a ticket",
                            },
                            "unit_amount": 3500,  # in cents
                        },
                        "quantity": 1
                    },
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "/success/",
                cancel_url=YOUR_DOMAIN + "/cancel/",
            )
            return JsonResponse({"id": checkout_session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})
