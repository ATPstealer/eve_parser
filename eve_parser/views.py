from django.shortcuts import render
from eve_parser.models import ParserStatus, ParserDateStatus


def stats(request):
    p = ParserDateStatus.objects.values_list("parser_name", "region_id", "region_id_log", "parse_time").order_by("parse_time")
    return render(request, 'eve_parser/stats.html', context={'statistics': p})


def stats2(request):
    p = ParserStatus.objects.values_list("name", "describe", "region_id", "now_parse")
    return render(request, 'eve_parser/stats2.html', context={'statistics': p})



