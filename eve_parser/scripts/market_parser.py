from eve_parser.include.parser import Parser
from eve_parser.models import Market, Regions
import json, asyncio, datetime


def run():
    coroutines = []
    for region in Regions.objects.values_list('region_id', flat=True):
        coroutines.append(paginator(region))
    print(coroutines)

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break


async def paginator(region):
    parser = Parser()
    for page in range(1, 10000):
        dict_get_args = {"order_type": "all", "page": page}
        market_json = parser.evetech_req("/markets/" + str(region) + "/orders/", dict_get_args)
        if 'error' in market_json:
            print(market_json)
            break
        insert_in_base(json.loads(market_json), region)
        await asyncio.sleep(0)


def insert_in_base(market_data, region):
    for order in market_data:
        m = list(Market.objects.filter(order_id=order["order_id"]))
        if len(m) < 1:
            market = Market.objects.create(
                order_id=order['order_id'], region_id=region, duration=order['duration'],
                is_buy_order=order['is_buy_order'], issued=order['issued'], location_id=order['location_id'],
                min_volume=order['min_volume'], price=order['price'], range=order['range'],system_id=order['system_id'],
                type_id=order['type_id'], volume_total=order['volume_total'], volume_remain=order['volume_remain'])
            market.save()
            print("Create: ", end='')
        else:
            market = Market.objects.filter(order_id=order["order_id"]).update(
                parse_time=datetime.datetime.now(datetime.timezone.utc),
                duration=order['duration'], is_buy_order=order['is_buy_order'], issued=order['issued'],
                location_id=order['location_id'], min_volume=order['min_volume'], price=order['price'],
                range=order['range'], system_id=order['system_id'], type_id=order['type_id'],
                volume_total=order['volume_total'], volume_remain=order['volume_remain'])
            print("Update: ", end='')

        print(str(region) + " " + str(order["order_id"]))