from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cashflow.settings.base import PAGE_TITLE

from customers.forms import CustomerOrderForm
from orders.models import CustomerOrder


# -------------------------------------  Customer Orders -------------------------------------
@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
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
