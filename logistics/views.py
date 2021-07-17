from django.shortcuts import render
from eve_parser.models import Liquidity, Types, Regions, LogisticsPlanning, ParserDateStatus
from logistics.models import models
from config import Config
from datetime import datetime


def liquidity(request):
    config = Config()
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
    count_display = 0
    liquidity_to_page = []
    for liq in liquidity_array:
        count_display += 1
        if count_display > config.counts_on_page:
            break
        name = Types.objects.values_list("name").filter(type_id=liq[0])
        liquidity_to_page.append({'name': name[0][0], 'type_id': liq[0], 'day_volume': "%.2f" % liq[1],
                                  'day_turnover': "%.2f" % liq[2], 'price': "%.2f" % liq[3]})

    regions = Regions.objects.values_list("name", "region_id").order_by("region_id")
    try:
        parse_time = ParserDateStatus.objects.values_list("parse_time").filter(parser_name="Liquidity calculation",
                                                                               region_id=region_id)
    except models.ObjectDoesNotExist:
        parse_time = ""
    print(parse_time[0][0])
    return render(request, 'logistics/liquidity.html', context={'region_selected': region, 'regions': regions,
                  'liquidity': liquidity_to_page, 'parse_time': parse_time})


def planing(request):
    config = Config()
    if "region_from" not in request.GET:
        region_from = "The Forge"
    else:
        region_from = request.GET["region_from"]
    try:
        region_id_from = Regions.objects.get(name=str(region_from)).region_id
    except models.ObjectDoesNotExist as e:
        region_id_from = 10000002
        region_from = "The Forge"

    if "region_to" not in request.GET:
        region_to = "Pure Blind"
    else:
        region_to = request.GET["region_to"]
    try:
        region_id_to = Regions.objects.get(name=str(region_to)).region_id
    except models.ObjectDoesNotExist as e:
        region_id_to = 10000023
        region_to = "Pure Blind"

    count_display = 0
    logistics_to_page = []
    if region_id_from < region_id_to:
        logistics_planing_array = LogisticsPlanning.objects.values_list(
            "type_id", "price_from", "price_to", "price_diff", "liquidity_from", "liquidity_to", "profit_from",
            "packaged_volume", "day_volume_to")\
            .filter(region_id_from=int(region_id_from), region_id_to=int(region_id_to)).order_by("-profit_from")
        for log in logistics_planing_array:
            count_display += 1
            if count_display > config.counts_on_page:
                break
            name = Types.objects.values_list("name").filter(type_id=log[0])
            logistics_to_page.append({'name': name[0][0], 'type_id': log[0], 'price_from': "%.2f" % log[1],
                                      'price_to': "%.2f" % log[2], 'price_diff': "%.2f" % log[3],
                                      'liquidity_from': "%.2f" % log[4], 'packaged_volume': "%.2f" % log[7],
                                      'liquidity_to': "%.2f" % log[5], 'profit_from': "%.2f" % log[6],
                                      'day_volume_to': "%.2f" % log[8]})
    else:
        # switch from and to
        logistics_planing_array = LogisticsPlanning.objects.values_list(
            "type_id", "price_from", "price_to", "price_diff", "liquidity_from", "liquidity_to", "profit_to",
            "packaged_volume", "day_volume_from")\
            .filter(region_id_from=int(region_id_to), region_id_to=int(region_id_from)).order_by("-profit_to")
        for log in logistics_planing_array:
            count_display += 1
            if count_display > config.counts_on_page:
                break
            name = Types.objects.values_list("name").filter(type_id=log[0])
            logistics_to_page.append({'name': name[0][0], 'type_id': log[0], 'price_from': "%.2f" % log[2],
                                      'price_to': "%.2f" % log[1], 'price_diff': "%.2f" % (-1 * log[3]),
                                      'liquidity_from': "%.2f" % log[5], 'packaged_volume': "%.2f" % log[7],
                                      'liquidity_to': "%.2f" % log[4], 'profit_from': "%.2f" % log[6],
                                      'day_volume_to': "%.2f" % log[8]})
    print(logistics_planing_array)
    regions = Regions.objects.values_list("name", "region_id").order_by("region_id")
    return render(request, 'logistics/planing.html',
                  context={'region_from_selected': region_from, 'region_to_selected': region_to,
                           'regions': regions, 'logistics': logistics_to_page})

