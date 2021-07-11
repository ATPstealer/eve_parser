from django.shortcuts import render
from eve_parser.models import Liquidity, Types


def liquidity(request):
    region_id = request.GET["region_id"]
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
        liquidity_to_page.append({'name': name[0][0], 'type_id': liq[0], 'day_volume': liq[1], 'day_turnover': liq[2], 'price': liq[3]})

    print(liquidity_to_page)

    return render(request, 'logistics/liquidity.html', context={'region_id': region_id, 'liquidity': liquidity_to_page})

