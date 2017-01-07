from django.shortcuts import render


# -------------------------------------  Branch offices -------------------------------------
def branch_offices(request):
    template = 'branchoffices/branch-offices.html'
    context = {
        'page_title': 'Dabbawala'
    }
    return render(request, template, context)
