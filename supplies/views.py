# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .forms import SupplyForm, CategoryForm
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


# -------------------------------------  Insumos ------------------------------------- 

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
	categories = Category.objects.order_by('name')
	providers  = Provider.objects.order_by('name')
	context    = {
		'categories':categories,
		'providers': providers,
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


# ------------------------------------- Categorias ------------------------------------- 

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


def new_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST, request.FILES)
		if form.is_valid():
			category = form.save(commit=False)
			category.save()
			return HttpResponseRedirect('/categories')
	else:
		form = CategoryForm()

	template   = loader.get_template('categories/new_category.html')
	page_title = 'Cash Flow'
	title      = 'Nueva Categoria'
	context    = {
		'form': form,
		'title': title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))


def categories_supplies(request, categ):
	category   = Category.objects.filter(name = categ)
	supply     = Supply.objects.filter(category = category)
	template   = loader.get_template('supplies/supplies.html')
	page_title = 'Cashflow'
	title      = categ
	context    = { 
		'supply' : supply,
		'title' : title,
		'page_title': page_title
	}
	return HttpResponse(template.render(context, request))