from django.shortcuts import render, redirect

from cashflow.settings.base import PAGE_TITLE
from customers.forms import CustomerOrderForm, CustomerProfileForm
from customers.models import CustomerOrder, CustomerProfile


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


# -------------------------------------  Customer Orders -------------------------------------
def customer_orders(request):
    customer_orders_objects = CustomerOrder.objects.all()
    template = 'customers/orders/orders.html'
    title = 'Realizar pedido'
    context = {
        'title': title,
        'customer_orders': customer_orders_objects,
        'page_title': PAGE_TITLE,
    }
    return render(request, template, context)


def new_customer_order(request):
    if request.method == 'POST':
        form = CustomerOrderForm(request.POST, request.FILES)
        if form.is_valid():
            customer_order = form.save(commit=False)
            customer_order.save()
            return redirect('customers:new_customer_order')
    else:
        form = CustomerOrderForm()

    template = 'customers/orders/new_order.html'
    title = 'DabbaNet - Nueva orden'
    context = {
        'form': form,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)
