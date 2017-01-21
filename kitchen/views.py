from django.shortcuts import render


# -------------------------------------  Kitchen -------------------------------------
from cashflow.settings.base import PAGE_TITLE
from kitchen.models import ProcessedProduct
from sales.models import Ticket, TicketDetail


def cold_kitchen(request):
    template = 'kitchen/cold.html'
    products = ProcessedProduct.objects.filter(status='PE')
    tickets = Ticket.objects.all()
    ticket_details = TicketDetail.objects.all()

    context = {
        'products': products,
        'tickets': tickets,
        'ticket_details': ticket_details,
        'page_title': PAGE_TITLE,
        'title': 'Cocina Fría'
    }

    return render(request, template, context)


def hot_kitchen(request):
    template = 'kitchen/hot.html'
    context = {}

    return render(request, template, context)


def assembly(request):
    template = 'kitchen/assembly.html'
    context = {}

    return render(request, template, context)
