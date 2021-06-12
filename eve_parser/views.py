from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404


def eve_pars(request):
    return HttpResponse("Hello world")
