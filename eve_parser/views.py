from django.shortcuts import render
from eve_parser.models import ParserStatus, ParserDateStatus


def stats(request):
    p = ParserDateStatus.objects.all().order_by('-parse_time').values_list()
    p[4] = p[4].strftime("%Y-%m-%d, %H:%M:%S")
    return render(request, 'eve_parser/stats.html', context={'statistics': p})


def stats2(request):
    p = ParserStatus.objects.values_list("name", "describe", "region_id", "now_parse")
    return render(request, 'eve_parser/stats2.html', context={'statistics': p})



