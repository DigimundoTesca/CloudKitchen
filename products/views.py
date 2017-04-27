# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required

from branchoffices.models import Supplier
from cloudkitchen.settings.base import PAGE_TITLE
from products.forms import SuppliesCategoryForm
from products.models import Cartridge, Supply, SuppliesCategory

from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import CreateView


# -------------------------------------  Profile -------------------------------------


# -------------------------------------  Providers -------------------------------------
@login_required(login_url='users:login')
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
@login_required(login_url='users:login')
def supplies(request):
    supplies_objects = Supply.objects.order_by('id')
    template = 'supplies/supplies.html'
    title = 'Insumos'

    context = {
        'supplies': supplies_objects,
        'title': PAGE_TITLE + ' | ' + title,
        'page_title': title,
    }
    return render(request, template, context)


class CreateSupply(CreateView):
    def __init__(self, **kwargs):
        self.object = None
        super(CreateSupply, self).__init__(**kwargs)

    model = Supply
    fields = ['name', 'category', 'barcode', 'supplier', 'storage_required', 'presentation_unit', 'presentation_cost',
              'measurement_quantity', 'measurement_unit', 'optimal_duration', 'optimal_duration_unit', 'location',
              'image']
    template_name = 'supplies/new_supply.html'

    def get_context_data(self, **kwargs):
        context = super(CreateSupply, self).get_context_data(**kwargs)
        title = 'Nuevo Insumo'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect('products:supplies')


class UpdateSupply(UpdateView):
    def __init__(self, **kwargs):
        self.object = None
        super(UpdateSupply, self).__init__(**kwargs)

    model = Supply
    fields = ['name', 'category', 'barcode', 'supplier', 'storage_required', 'presentation_unit', 'presentation_cost',
              'measurement_quantity', 'measurement_unit', 'optimal_duration', 'optimal_duration_unit', 'location',
              'image']
    template_name = 'supplies/new_supply.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateSupply, self).get_context_data(**kwargs)
        title = 'Modificar Insumo'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    def form_valid(self, form):
        print(form)
        self.object = form.save()
        return redirect('products:supplies')


class DeleteSupply(DeleteView):
    def __init__(self, **kwargs):
        self.object = None
        super(DeleteSupply, self).__init__(**kwargs)

    model = Supply
    template_name = 'supplies/delete_supply.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteSupply, self).get_context_data(**kwargs)
        title = 'Eliminar Insumo'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('products:supplies')


@login_required(login_url='users:login')
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
@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
def new_category(request):
    if request.method == 'POST':
        form = SuppliesCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('products:categories')
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


@login_required(login_url='users:login')
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
@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
def cartridge_detail(request, pk):
    cartridge = get_object_or_404(Cartridge, pk=pk)
    template = 'cartridges/cartridge_detail.html'
    title = 'DabbaNet - Detalles del Producto'
    context = {
        'page_title': PAGE_TITLE,
        'cartridge': cartridge,
        'title': title
    }
    return render(request, template, context)


class CreateCartridge(CreateView):
    def __init__(self, **kwargs):
        self.object = None
        super(CreateCartridge, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateCartridge, self).get_context_data(**kwargs)
        title = 'Crear Producto'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    model = Cartridge
    fields = ['name', 'price', 'category', 'image']
    template_name = 'cartridges/new_cartridge.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect('products:cartridges')


class UpdateCartridge(UpdateView):
    def __init__(self, **kwargs):
        self.object = None
        super(UpdateCartridge, self).__init__(**kwargs)

    model = Cartridge
    fields = ['name', 'price', 'category', 'image']
    template_name = 'cartridges/new_cartridge.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateCartridge, self).get_context_data(**kwargs)
        title = 'Actualizar Producto'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect('products:cartridges')


class DeleteCartridge(DeleteView):
    def __init__(self, **kwargs):
        self.object = None
        super(DeleteCartridge, self).__init__(**kwargs)

    model = Cartridge
    template_name = 'cartridges/delete_cartridge.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteCartridge, self).get_context_data(**kwargs)
        title = 'Eliminar Producto'
        context['title'] = PAGE_TITLE + ' | ' + title
        context['page_title'] = title
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('products:cartridges')


# -------------------------------------  Test -------------------------------------

def test(request):
    # template = 'base/base_nav_footer.html'
    template = 'base/nav.html'
    return render(request, template, {})
