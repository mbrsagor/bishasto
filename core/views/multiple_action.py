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


