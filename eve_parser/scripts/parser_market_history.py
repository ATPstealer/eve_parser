from eve_parser.include.parser import Parser
from eve_parser.models import TopTypes, Types, Regions, MarketHistory
import json
from datetime import datetime


def run(*args):
    start = datetime.now()
    if len(args) == 0:
        for region in Regions.objects.values_list("region_id"):
            parse_region_history(region)
    else:
        parse_region_history(args)
    print("start at: %s\n end at: %s" % (start, datetime.now()))
    Parser.parser_status("Market history", "Done \nStart at: %s\n end at: %s" % (start, datetime.now()), 0, 0)


def parse_region_history(args):
    parser = Parser()
    region = args[0]
    if len(args) > 1:
        if "all" in args[1]:
            parse_type_array = Types.objects.values_list("type_id")
        else:
            parse_type_array = TopTypes.objects.values_list("type_id")
    else:
        parse_type_array = TopTypes.objects.values_list("type_id")
    print("Region parse start: " + str(region))
    for item_type in parse_type_array:
        dict_get_args = {"type_id": item_type[0]}
        market_history_json = parser.evetech_req("/markets/" + str(region) + "/history/", dict_get_args)
        if "error" in market_history_json:
            continue
        Parser.parser_status("Market history", "item_type", region, item_type[0])
        print("Item: " + str(region) + " " + str(item_type[0]))
        insert_in_base(json.loads(market_history_json), region, item_type[0])


def insert_in_base(market_history_data, region, item_type):
    market_history_exist = list(MarketHistory.objects.filter(region_id=region, type_id=item_type))
    for market_history_day in market_history_data:
        day_exist = 0
        for day_in_base in market_history_exist:
            if market_history_day["date"] == str(day_in_base.date):
                day_exist = 1
                break
        if not day_exist:
            market_history = MarketHistory.objects.create(
                region_id=region, type_id=item_type,
                date=market_history_day['date'], average=market_history_day['average'],
                highest=market_history_day['highest'], lowest=market_history_day['lowest'],
                order_count=market_history_day['order_count'], volume=market_history_day['volume'])
            market_history.save()
