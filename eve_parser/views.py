from django.shortcuts import render
from eve_parser.models import ParserStatus


def stats(request):
    p = ParserStatus.objects.values_list("name", "describe", "region_id", "now_parse")
    return render(request, 'eve_parser/stats.html', context={'statistics': p})



