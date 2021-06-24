from django.http import HttpResponse, Http404
from django.shortcuts import redirect
import datetime

from eve_parser.views import stats


def hello(request):
    return HttpResponse("Hello world")


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def hours_ahead(request, num):
    html = "it %s" % (num)
    return HttpResponse(html)


def redirect_pars(request):
    return redirect(stats)
