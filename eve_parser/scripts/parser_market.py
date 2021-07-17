from eve_parser.include.parser import Parser
from eve_parser.models import Market, Regions
import json
from datetime import datetime, timezone, timedelta


def run(*args):
    Parser.parser_date_status("START Market", 0, 0)
    start = datetime.now()
    if len(args) == 0:
        for region in Regions.objects.values_list('region_id', flat=True):
            paginator(region)
    else:
        paginator(args[0])
    print("start at: %s\n end at: %s" % (start, datetime.now()))
    clear_market()
    Parser.parser_date_status("END Market", 0, 0)


def paginator(region):
    parser = Parser()
    for page in range(1, 10000):
        dict_get_args = {"order_type": "all", "page": page}
        market_json = parser.evetech_req("/markets/" + str(region) + "/orders/", dict_get_args)
        if 'error' in market_json:
            print(market_json)
            break
        print("Parse market in " + str(region) + " page " + str(page))
        insert_in_base(json.loads(market_json), region)
    Parser.parser_date_status("Market", region, 0)


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
        else:
            market = Market.objects.filter(order_id=order["order_id"]).update(
                parse_time=datetime.now(timezone.utc),
                duration=order['duration'], is_buy_order=order['is_buy_order'], issued=order['issued'],
                location_id=order['location_id'], min_volume=order['min_volume'], price=order['price'],
                range=order['range'], system_id=order['system_id'], type_id=order['type_id'],
                volume_total=order['volume_total'], volume_remain=order['volume_remain'])


def clear_market():
    orders_for_delete = Market.objects.filter(parse_time__lte=datetime.now(timezone.utc) - timedelta(days=1))
    for order in orders_for_delete:
        print("Delete: " + str(order.order_id))
        order.delete()

