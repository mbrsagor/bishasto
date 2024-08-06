from django.contrib import messages
from django.shortcuts import redirect, render
from engine.forms.engine_utils_form import FuelTypeModelForm
from engine.models import Fuel
from engine.forms.fuel_form import FuelModelForm


def fuel_create_view(request):
    success_message = 'Fuel has been created successfully.'
    template_name = 'fuel/create_fuel.html'

    if request.method == 'POST' and 'add_fuel' in request.POST:
        form = FuelModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.INFO, success_message)
            return redirect('create_fuel')
    else:
        form = FuelModelForm(request.POST)
    if request.method == 'POST' and 'fuel_form' in request.POST:
        fuel_from = FuelTypeModelForm(request.POST)
        if fuel_from.is_valid():
            instance = fuel_from.save(commit=False)
            instance.save()
            messages.add_message(request, messages.INFO, "Fuel type added.")
            return redirect('create_fuel')
    else:
        fuel_from = FuelTypeModelForm()
    context = {
        'form': form,
        'fuel_from': fuel_from
    }
    return render(request, template_name, context)


class VerifyTicketAPIView(views.APIView):
    """
    Name: Guard can verify ticket
    Desc: Guard can verify ticket and send email to company
    URL: /api/v1/event/verify-ticket/
    Methods: PUT
    :param: event_id, ticket_number
    :return
    """

    def get(self, request, *args, **kwargs):
        # Get data from request
        event_id = self.request.query_params.get('event_id')
        ticket_number = self.request.query_params.get('ticket_number')

        try:
            event = Event.objects.get(id=event_id)
            ticket = event.eventTicket.get(ticket_number=ticket_number)
            # Verify ticket
            verify_ticket = Ticket.objects.get(ticket_number=ticket)
            if verify_ticket.is_active == False and verify_ticket.is_scanned == False:
                verify_ticket.is_active = True
                verify_ticket.is_scanned = True
                verify_ticket.save()
                resp = {
                    "status": "success",
                    "message": messages.VERIFY_SUCCESS_TICKET,
                    "is_verified": True,
                }
                return Response(resp, status=status.HTTP_200_OK)
            resp2 = {
                    "status": "success",
                    "message": messages.VERIFY_FAILED_TICKET,
                    "is_verified": False,
                }
            return Response(resp2, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response(responses.prepare_error_response(messages.TICKET_NOT_MATCH), status=status.HTTP_200_OK)
