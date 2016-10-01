from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .forms import SupplyForm
from .models import Provider, Category, Supply

def login(request):
	supply     = Supply.objects.order_by('id')
	template   = loader.get_template('auth/login.html')
	page_title = 'Cashflow'
	title      = 'Iniciar Sesión'
	context    = {
		'page_title' : page_title,
		'title' : title
	}
	return HttpResponse(template.render(context, request))


def index(request):
	template   = loader.get_template('index.html')
	page_title = 'Cashflow'
	title      = 'Bienvenido'
	context    = {
		'page_title' : page_title,
		'title' : title
	}
	return HttpResponse(template.render(context, request))


def supplies(request):
	supply     = Supply.objects.order_by('id')
	template   = loader.get_template('supplies/supplies.html')
	page_title = 'Cashflow'
	title      = 'Insumos'
	context    = { 
		'supply' : supply,
		'title' : title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))


def new_supply(request):
	if request.method == 'POST':
		form = SupplyForm(request.POST, request.FILES)
		if form.is_valid():
			supply = form.save(commit=False)
			supply.save()
			return HttpResponseRedirect('/supplies')
	else:
		form = SupplyForm()

	template   = loader.get_template('supplies/new_supply.html')
	page_title = 'Cash Flow'
	title      = 'Nuevo insumo'
	context    = {
		'form': form,
		'title': title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))


def supply_detail(request, pk):
	supply  = get_object_or_404(Supply, pk=pk)
	template = loader.get_template('supplies/supply_detail.html')
	title    = 'Detalles del insumo'
	context  = {
		'supply'	: supply,
		'title'		: title
	}

	return HttpResponse(template.render(context, request))



def categories(request):
	category   = Category.objects.order_by('id')
	template   = loader.get_template('categories/categories.html')
	page_title = 'Cashflow'
	title      = 'Categorias'
	context    = { 
		'category' : category,
		'title' : title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))


def categories_supplies(request, category):
	category   = Category.objects.filter(name = category)
	supply     = Supply.objects.filter(category = category)
	template   = loader.get_template('supplies/supplies.html')
	page_title = 'Cashflow'
	title      = 'Categorias'
	context    = { 
		'supply' : supply,
		'title' : title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))