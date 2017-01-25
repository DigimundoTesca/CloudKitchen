import json
from datetime import datetime, date, timedelta

from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


from branchoffices.models import CashRegister
from cashflow.settings.base import PAGE_TITLE
from products.models import Cartridge, PackageCartridge, PackageCartridgeRecipe
from sales.models import Ticket, TicketDetail
from users.models import User as UserProfile


# -------------------------------------  Sales -------------------------------------
@login_required(login_url='users:login')
def sales(request):
    def get_name_day():
        datetime_now = datetime.now()
        days_list = {
            'MONDAY': 'Lunes',
            'TUESDAY': 'Martes',
            'WEDNESDAY': 'Miércoles',
            'THURSDAY': 'Jueves',
            'FRIDAY': 'Viernes',
            'SATURDAY': 'Sábado',
            'SUNDAY': 'Domingo'
        }
        name_day = date(datetime_now.year, datetime_now.month, datetime_now.day)
        return days_list[name_day.strftime('%A').upper()]

    def get_number_day():
        days = {
            'Lunes': 1, 'Martes': 2, 'Miércoles': 3, 'Jueves': 4, 'Viernes': 5, 'Sábado': 6, 'Domingo': 7,
        }
        return days[get_name_day()]

    def get_week_number():
        return date.today().isocalendar()[1]

    def get_sales_week():
        total_earnings = 0
        week_sales_list = [0, 0, 0, 0, 0, 0, 0]
        days_to_count = get_number_day() - 1
        day_limit = days_to_count
        start_date_number = 0

        while start_date_number <= day_limit:
            start_date = date.today() - timedelta(days=days_to_count)
            end_date = start_date + timedelta(days=1)
            tickets = Ticket.objects.filter(created_at__range=[start_date, end_date])

            for ticket in tickets:
                ticket_details = TicketDetail.objects.filter(ticket=ticket)

                for ticket_detail in ticket_details:
                    total_earnings += ticket_detail.price

            week_sales_list[start_date_number] = float(total_earnings)

            # restarting counters
            days_to_count -= 1
            total_earnings = 0
            start_date_number += 1
        return json.dumps(week_sales_list)

    def get_sales_day():
        days = get_number_day()
        return days

    def get_tickets():
        tickets_object = Ticket.objects.all()
        return tickets_object

    def get_tickets_details():
        tickets = []
        for ticket_object in Ticket.objects.all():
            ticket_detail = {
                'id_parent': ticket_object,
                'details': [],
                'total': 0.0,
                'quantity': 0.0
            }
            for ticket_detail_object in TicketDetail.objects.filter(ticket=ticket_object.id):
                ticket_detail['details'].append(ticket_detail_object)
                ticket_detail['total'] += float(ticket_detail_object.price)
                ticket_detail['quantity'] += float(ticket_detail_object.quantity)
            tickets.append(ticket_detail)
        return tickets

    template = 'sales/sales.html'
    title = 'Ventas'
    context = {
        'page_title': PAGE_TITLE,
        'title': title,
        'week_earnings': get_sales_week(),
        'day_earnings': get_sales_day(),
        'day': get_name_day(),
        'week': get_week_number(),
        'tickets': get_tickets(),
        'ticket_details': get_tickets_details(),
    }

    return render(request, template, context)


@login_required(login_url='users:login')
def get_sales_day_view(request):
    def get_name_day():
        datetime_now = datetime.now()
        days_list = {
            'MONDAY': 'Lunes',
            'TUESDAY': 'Martes',
            'WEDNESDAY': 'Miércoles',
            'THURSDAY': 'Jueves',
            'FRIDAY': 'Viernes',
            'SATURDAY': 'Sábado',
            'SUNDAY': 'Domingo'
        }
        name_day = datetime.date(datetime_now.year, datetime_now.month, datetime_now.day)
        return days_list[name_day.strftime('%A').upper()]

    def get_sales_day(filter_date):
        start_date = date.today() - timedelta(days=4)
        end_date = start_date + timedelta(days=1)
        tickets = Ticket.objects.filter(created_at__range=[start_date, end_date])

    return JsonResponse({'day': get_name_day()})


@login_required(login_url='users:login')
def new_sale(request):
    if request.method == 'POST':
        if request.POST['ticket']:
            username = request.user
            user_profile_object = get_object_or_404(UserProfile, username=username)
            cash_register = CashRegister.objects.first()
            new_ticket_object = Ticket(cash_register=cash_register, seller=user_profile_object, )
            new_ticket_object.save()
            ticket_detail_json_object = json.loads(request.POST.get('ticket'))

            """
            Saves the tickets details for cartridges
            """
            for ticket_detail in ticket_detail_json_object['cartuchos']:
                cartridge_object = get_object_or_404(Cartridge, id=ticket_detail['id'])
                quantity = ticket_detail['cant']
                price = ticket_detail['price']
                new_ticket_detail_object = TicketDetail(
                    ticket=new_ticket_object,
                    cartridge=cartridge_object,
                    quantity=quantity,
                    price=price
                )
                new_ticket_detail_object.save()

            """
            Saves the tickets details for package cartridges
            """
            print(ticket_detail_json_object['paquetes'])
            for ticket_detail in ticket_detail_json_object['paquetes']:
                quantity = ticket_detail['quantity']
                price = ticket_detail['price']

                packages_lists = []
                package_list = []
                index_packages_lists = 0
                package_id = None
                new_package = True

                """
                Gets the packages that already have the chosen products
                """
                for id_cartridge in ticket_detail['id_list']:
                    packages_recipe = PackageCartridgeRecipe.objects.filter(cartridge=id_cartridge)
                    packages_lists.append([])

                    for package_recipe in packages_recipe:
                        packages_lists[index_packages_lists].append(package_recipe.package_cartridge.id)

                    index_packages_lists += 1

                for element in packages_lists:
                    package_list += element

                """
                Validates if it's a new package
                """
                list_1 = packages_lists[0]
                list_2 = packages_lists[1]
                list_3 = packages_lists[2]


                # TO FIX - RAMSES
                for x in list_1:
                    if new_package:
                        for y in list_2:
                            if x == y:
                                for z in list_3:
                                    if x == y == z:
                                        new_package = False
                                        package_id = x

                if new_package:
                    package_name = ticket_detail['name']
                    package_price = ticket_detail['price']
                    new_package_object = PackageCartridge(name=package_name, price=package_price, package_active=True)
                    new_package_object.save()

                    """
                    Creates a new package
                    """
                    for id_cartridge in ticket_detail['id_list']:
                        cartridge_object = get_object_or_404(Cartridge, id=id_cartridge)
                        new_package_recipe_object = PackageCartridgeRecipe(
                            package_cartridge=new_package_object,
                            cartridge=cartridge_object,
                            quantity=1
                        )
                        new_package_recipe_object.save()

                    """
                    Creates the ticket detail
                    """
                    new_ticket_detail_object = TicketDetail(
                        ticket=new_ticket_object,
                        package_cartridge=new_package_object,
                        quantity=quantity,
                        price=price
                    )
                    new_ticket_detail_object.save()

                else:
                    """
                    Uses an existent package
                    """
                    package_object = get_object_or_404(PackageCartridge, id=package_id)
                    new_ticket_detail_object = TicketDetail(
                        ticket=new_ticket_object,
                        package_cartridge=package_object,
                        quantity=quantity,
                        price=price,
                    )
                    new_ticket_detail_object.save()

            data = {
                'status': 'ready'
            }
            return JsonResponse(data)

    else:
        cartridges_list = Cartridge.objects.all()
        package_cartridges = PackageCartridge.objects.all()
        template = 'sales/new_sale.html'
        title = 'Nueva venta'
        context = {
            'page_title': PAGE_TITLE,
            'title': title,
            'cartridges': cartridges_list,
            'package_cartridges': package_cartridges
        }
    return render(request, template, context)
