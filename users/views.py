from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from supplies.views import PAGE_TITLE


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

