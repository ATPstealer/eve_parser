from django.shortcuts import render
from eve_parser.models import Liquidity, Types, Regions
from logistics.models import models
import operator


def liquidity(request):
    if "region" not in request.GET:
        region = "The Forge"
    else:
        region = request.GET["region"]
    try:
        region_id = Regions.objects.get(name=str(region)).region_id
    except models.ObjectDoesNotExist as e:
        region_id = 10000002
        region = "The Forge"

    liquidity_array = Liquidity.objects.values_list("type_id", "day_volume", "day_turnover", "price").\
        filter(region_id=int(region_id)).order_by("-day_turnover")
    print(liquidity_array)
    count_display = 0
    liquidity_to_page = []
    for liq in liquidity_array:
        count_display += 1
        if count_display > 100:
            break
        name = Types.objects.values_list("name").filter(type_id=liq[0])
        liquidity_to_page.append({'name': name[0][0], 'type_id': liq[0], 'day_volume': liq[1],
                                  'day_turnover': liq[2], 'price': liq[3]})

    regions = Regions.objects.values_list("name", "region_id").order_by("region_id")
    return render(request, 'logistics/liquidity.html',
                  context={'region_selected': region, 'regions': regions, 'liquidity': liquidity_to_page})


def planing(request):
    return render(request, 'logistics/planing.html', context={})
