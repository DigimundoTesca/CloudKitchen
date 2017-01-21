from django.shortcuts import render


# -------------------------------------  Kitchen -------------------------------------
from cashflow.settings.base import PAGE_TITLE
from kitchen.models import ProcessedProduct
from sales.models import Ticket, TicketDetail


def cold_kitchen(request):
    template = 'kitchen/cold.html'
    tickets = Ticket.objects.all()

    def get_processed_products():
        processed_products_list = []
        processed_product_object = {
            'ticket_id': None,
            'cartridges': None,
            'packages': None,
        }
        processed_objects = ProcessedProduct.objects.filter(status='PE')
        for processed in processed_objects:
            processed_product_object['ticket_id'] = processed.id
            print(1)
        print(processed_product_object)
        return processed_products_list

    print(get_processed_products())
    context = {
        #'products': products,
        'tickets': tickets,
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
