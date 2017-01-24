from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# -------------------------------------  Kitchen -------------------------------------
from cashflow.settings.base import PAGE_TITLE
from kitchen.models import ProcessedProduct
from products.models import PackageCartridgeRecipe
from sales.models import Ticket, TicketDetail


@login_required(login_url='users:login')
def cold_kitchen(request):
    template = 'kitchen/cold.html'
    tickets = Ticket.objects.all()

    def get_processed_products():
        processed_products_list = []
        processed_objects = ProcessedProduct.objects.filter(status='PE')

        for processed in processed_objects:
            processed_product_object = {
                'ticket_id': processed.ticket,
                'cartridges': [],
                'packages': []
            }

            for ticket_detail in TicketDetail.objects.filter(ticket=processed.ticket):
                if ticket_detail.ticket == processed.ticket:
                    if ticket_detail.cartridge:
                        cartridge = {
                            'quantity': ticket_detail.quantity,
                            'cartridge': ticket_detail.cartridge
                        }
                        processed_product_object['cartridges'].append(cartridge)

                    elif ticket_detail.package_cartridge:
                        package = {
                            'quantity': ticket_detail.quantity,
                            'package_recipe': []
                        }
                        package_recipe = \
                            PackageCartridgeRecipe.objects.filter(package_cartridge=ticket_detail.package_cartridge)
                        for recipe in package_recipe:
                            package['package_recipe'].append(recipe.cartridge)
                        processed_product_object['packages'].append(package)

            processed_products_list.append(processed_product_object)
        return processed_products_list
    for xd in get_processed_products():
        pass
    context = {
        'products': get_processed_products(),
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
