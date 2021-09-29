from django.shortcuts import render


def index(request):
    return render(request, 'eve/index.html', context={'title': 'eve stats'})

