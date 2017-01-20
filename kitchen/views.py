from django.shortcuts import render


# -------------------------------------  Kitchen -------------------------------------
def cold_kitchen(request):
    template = 'kitchen/cold.html'
    context = {}

    return render(request, template, context)


def hot_kitchen(request):
    template = 'kitchen/hot.html'
    context = {}

    return render(request, template, context)


def assembly(request):
    template = 'kitchen/hot.html'
    context = {}

    return render(request, template, context)
