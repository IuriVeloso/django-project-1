from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', context={'name': 'Iuri Veloso'})

# Create your views here.
