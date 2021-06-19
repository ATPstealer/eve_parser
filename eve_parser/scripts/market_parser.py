from eve_parser.include.parser import Parser
from eve_parser.models import Market, Regions
import json


def run():
    for region in Regions.objects.values_list('region_id', flat=True):
        paginator(region)



def paginator(region):
    parser = Parser()
    for page in range(1, 2):
        dict_get_args = {"order_type": "all", "page": page}
        market_json = parser.evetech_req("/markets/" + str(region) + "/orders/", dict_get_args)
        if 'error' in market_json:
            print(market_json)
            break
        insert_in_base(json.loads(market_json))


def insert_in_base(market_data):
    for order in market_data:
        exist = 0
        exist_markets = Market.objects.values_list('order_id')
        for exist_market in exist_markets:
            if order['order_id'] == exist_market[0]:
                exist = 1
                break

        if exist == 0:
            market = Market.objects.create(order_id=order['order_id'], duration=order['duration'],
                                           is_buy_order=order['is_buy_order'], issued=order['issued'] ,
                                           location_id=order['location_id'], min_volume=order['min_volume'],
                                           price=order['price'], range=order['range'],
                                           system_id=order['system_id'], type_id=order['type_id'],
                                           volume_total=order['volume_total'], volume_remain=order['volume_remain'])
            market.save()



