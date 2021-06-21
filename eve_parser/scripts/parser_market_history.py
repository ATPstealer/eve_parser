from eve_parser.include.parser import Parser
from eve_parser.models import Types, Regions, MarketHistory
import json
from datetime import datetime, timezone


def run():
    start = datetime.now()
    parser = Parser()
    for region in Regions.objects.values_list("region_id"):
        for item_type in Types.objects.values_list("type_id"):
            dict_get_args = {"type_id": item_type[0]}
            market_history_json = parser.evetech_req("/markets/" + str(region[0]) + "/history/", dict_get_args)
            if "error" in market_history_json:
                continue
            insert_in_base(json.loads(market_history_json), region[0], item_type[0])
    print("start at: %s\nend at: %s" % (start, datetime.now()))


def insert_in_base(market_history_data, region, item_type):
    for market_history_day in market_history_data:
        m = list(MarketHistory.objects.filter(region_id=region, type_id=item_type, date=market_history_day['date']))
        print("Skip: " + str(region) + " " + str(item_type) + " " + market_history_day['date'])
        if len(m) == 0:
            print("Create: " + str(region) + " " + str(item_type) + " " + market_history_day['date'])
            market_history = MarketHistory.objects.create(
                region_id=region, type_id=item_type,
                date=market_history_day['date'], average=market_history_day['average'],
                highest=market_history_day['highest'], lowest=market_history_day['lowest'],
                order_count=market_history_day['order_count'], volume=market_history_day['volume'])
            market_history.save()
