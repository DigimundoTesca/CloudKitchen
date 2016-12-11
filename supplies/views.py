# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json
import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

PAGE_TITLE = 'DabbaNet'


def test(request):
    template = '500.html'
    return render(request, template, {})


# -------------------------------------  Auth -------------------------------------
def login(request):
    if request.user.is_authenticated():
        return redirect('supplies:sales')

    message = None
    template = 'auth/login.html'

    if request.method == 'POST':
        username_post = request.POST.get('username_login')
        password_post = request.POST.get('password_login')
        user = authenticate(username=username_post, password=password_post)

        if user is not None:
            login_django(request, user)
            return redirect('supplies:sales')

        else:
            message = 'Usuario o contraseña incorrecto'

    context = {
        'page_title': PAGE_TITLE,
        'message': message
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def logout(request):
    logout_django(request)
    return redirect('supplies:login')


# -------------------------------------  Profile -------------------------------------


# -------------------------------------  Sales -------------------------------------
@login_required(login_url='supplies:login')
def sales(request, total_earnings=0):

    def calc_day():
        datetime_now = datetime.datetime.now()

        days_list = {
            'MONDAY': 'Lunes',
            'TUESDAY': 'Martes',
            'WEDNESDAY': 'Miercoles',
            'THURSDAY': 'Jueves',
            'FRIDAY': 'Viernes',
            'SATURDAY': 'Sabado',
            'SUNDAY': 'Domingo'
        }

        name_day = datetime.date(datetime_now.year, datetime_now.month, datetime_now.day)
        return days_list[name_day.strftime('%A').upper()]

    ticket_details = TicketDetail.objects.all()
    for ticket in ticket_details:
        total_earnings += ticket.price

    template = 'sales/sales.html'
    title = 'Ventas'
    context = {
        'page_title': PAGE_TITLE,
        'title': title,
        'earnings': total_earnings,
        'day': calc_day(),
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def new_sale(request):
    if request.method == 'POST':
        username = request.user
        user = User.objects.filter(username=username)
        user_profile = UserProfile.objects.get(user=user)
        cash_register = CashRegister.objects.first()
        new_ticket = Ticket(cash_register=cash_register, seller=user_profile, )
        new_ticket.save()
        ticket_detail_json_object = json.loads(request.POST.get('ticket'))

        # save the tickets details for cartridges
        for ticket_detail in ticket_detail_json_object['cartuchos']:
            cartridge = Cartridge.objects.get(id=ticket_detail['id'])
            quantity = ticket_detail['cant']
            price = ticket_detail['price']
            new_ticket_detail = TicketDetail(ticket=new_ticket, cartridge=cartridge, quantity=quantity, price=price)
            new_ticket_detail.save()

        # save the tickets details for package cartridges
        for ticket_detail in ticket_detail_json_object['paquetes']:
            package_cartridge = PackageCartridge.objects.get(id=ticket_detail['id'])
            quantity = ticket_detail['cant']
            price = ticket_detail['price']
            new_ticket_detail = TicketDetail(ticket=new_ticket, package_cartridge=package_cartridge, quantity=quantity,
                                             price=price)
            new_ticket_detail.save()

        data = {
            'status': 'listo'
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


# -------------------------------------  Providers -------------------------------------
@login_required(login_url='supplies:login')
def suppliers(request):
    suppliers_list = Supplier.objects.order_by('id')
    template = 'suppliers/suppliers.html'
    title = 'Proveedores'
    context = {
        'suppliers': suppliers_list,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


# -------------------------------------  Supplies -------------------------------------
@login_required(login_url='supplies:login')
def supplies(request):
    supply = Supply.objects.order_by('id')
    template = 'supplies/supplies.html'
    title = 'Insumos'
    context = {
        'supplies': supply,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def new_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST, request.FILES)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.save()
            return redirect('/supplies/')
    else:
        form = SupplyForm()

    template = 'supplies/new_supply.html'
    title = 'DabbaNet - Nuevo insumo'
    categories_list = SuppliesCategory.objects.order_by('name')
    suppliers_list = Supplier.objects.order_by('name')
    context = {
        'categories': categories_list,
        'suppliers': suppliers_list,
        'form': form,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def supply_detail(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    template = 'supplies/supply_detail.html'
    title = 'DabbaNet - Detalles del insumo'
    context = {
        'page_title': PAGE_TITLE,
        'supply': supply,
        'title': title
    }
    return render(request, template, context)


# ------------------------------------- Categories ------------------------------------- 
@login_required(login_url='supplies:login')
def categories(request):
    supplies_categories = SuppliesCategory.objects.order_by('id')
    template = 'categories/categories.html'
    title = 'Categorias'
    context = {
        'supplies_categories': supplies_categories,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def new_category(request):
    if request.method == 'POST':
        form = SuppliesCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('/categories')
    else:
        form = SuppliesCategoryForm()

    template = 'categories/new_category.html'
    title = 'Nueva Categoria'
    context = {
        'form': form,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def categories_supplies(request, categ):
    supplies_categories = SuppliesCategoryForm.objects.filter(name=categ)
    supply = Supply.objects.filter(category=supplies_categories)
    template = 'supplies/supplies.html'
    title = categ
    context = {
        'supply': supply,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


# -------------------------------------  Cartridges ------------------------------------- 
@login_required(login_url='supplies:login')
def cartridges(request):
    cartridges_list = Cartridge.objects.order_by('id')
    template = 'cartridges/cartridges.html'
    title = 'Cartuchos'
    context = {
        'cartridges': cartridges_list,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)


@login_required(login_url='supplies:login')
def new_cartridge(request):
    if request.method == 'POST':
        form = CartridgeForm(request.POST, request.FILES)
        if form.is_valid():
            cartridge = form.save(commit=False)
            cartridge.save()
            return redirect('/cartridges')
    else:
        form = CartridgeForm()

    template = 'cartridges/new_cartridge.html'
    title = 'Nuevo Cartucho'
    context = {
        'form': form,
        'title': title,
        'page_title': PAGE_TITLE
    }
    return render(request, template, context)
