from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cashflow.settings.base import PAGE_TITLE
from customers.forms import CustomerProfileForm
from customers.models import CustomerProfile


# -------------------------------------  Customers -------------------------------------

def new_customer(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('customers:thanks')
    else:
        form = CustomerProfileForm()

    template = 'customers/register/new_customer.html'
    title = 'Dabbawala - Registro de clientes'

    context = {
        'form': form,
        'title': title,
    }

    return render(request, template, context)


def thanks(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('customers:new_customer')
    else:
        form = CustomerProfileForm()

    template = 'customers/register/thanks.html'
    title = 'Dabbawala - Registro de clientes'

    context = {
        'form': form,
        'title': title,
    }

    return render(request, template, context)


@login_required(login_url='users:login')
def customers_list(request):
    template = 'customers/register/customers_list.html'
    customers = CustomerProfile.objects.all()
    title = 'Clientes registrados'

    context = {
        'title': title,
        'page_title': PAGE_TITLE,
        'customers': customers,
    }

    return render(request, template, context)
