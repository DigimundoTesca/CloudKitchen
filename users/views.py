from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from users.forms import CustomerProfileForm, UserProfileForm

from cashflow.settings.base import PAGE_TITLE


# -------------------------------------  Index -------------------------------------
from users.models import CustomerProfile


def test(request):
    form_customer = CustomerProfileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form_customer.is_valid():
            print('IS VALID!!!')
            customer = form_customer.save(commit=False)
            customer.save()
            return redirect('users:thanks')
        print('IS NOT VALID!!!')
    else:
        print('IS NOT POST')
        form_customer = CustomerProfileForm()
    template = 'test/test.html'
    title = 'Dabbawala - Registro de clientes'
    form_user = UserProfileForm()
    context = {
        'form_user': form_user,
        'form_customer': form_customer,
        'title': title,
    }

    return render(request, template, context)


# -------------------------------------  Index -------------------------------------
def index(request):
    template = 'index.html'
    context = {
        'page_title': PAGE_TITLE,
    }
    return redirect('users:new_customer')


# -------------------------------------  Auth -------------------------------------
def login(request):
    if request.user.is_authenticated():
        return redirect('sales:sales')

    message = None
    template = 'auth/login.html'

    if request.method == 'POST':
        username_post = request.POST.get('username_login')
        password_post = request.POST.get('password_login')
        user = authenticate(username=username_post, password=password_post)

        if user is not None:
            login_django(request, user)
            return redirect('sales:sales')

        else:
            message = 'Usuario o contraseña incorrecto'

    context = {
        'page_title': PAGE_TITLE,
        'message': message,
    }
    return render(request, template, context)


@login_required(login_url='users:login')
def logout(request):
    logout_django(request)
    return redirect('users:login')


# -------------------------------------  Customers -------------------------------------
def new_customer(request):
    if request.method == 'POST':
        form_customer = CustomerProfileForm(request.POST, request.FILES)
        if form_customer.is_valid():
            customer = form_customer.save(commit=False)
            customer.save()
            return redirect('users:thanks')
    else:
        form_customer = CustomerProfileForm()

    template = 'customers/register/new_customer.html'
    title = 'Dabbawala - Registro de clientes'
    form_user = UserProfileForm()
    context = {
        'form_user': form_user,
        'form_customer': form_customer,
        'title': title,
    }

    return render(request, template, context)


def thanks(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('users:new_customer')
    else:
        form = CustomerProfileForm()

    template = 'customers/register/thanks.html'
    title = 'Dabbawala - Registro de clientes'

    context = {
        'form': form,
        'title': title,
    }

    return render(request, template, context)


@login_required(login_url='users:login')
def customers_list(request):
    template = 'customers/register/customers_list.html'
    customers = CustomerProfile.objects.all()
    title = 'Clientes registrados'

    context = {
        'title': title,
        'page_title': PAGE_TITLE,
        'customers': customers,
    }

    return render(request, template, context)
