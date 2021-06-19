# Create your views here.
from django.http import HttpResponse
from eve_parser.include.parser import Parser


def eve_pars(request):
    parser = Parser()
    parse_json = parser.evetech_req("/universe/regions/")
    return HttpResponse(parse_json)
