from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from eve_parser.parser import Parser


def eve_pars(request):
    parser = Parser()
    parser.make_something()
    return HttpResponse("text")
