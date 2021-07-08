from eve_parser.models import TopTypes, Regions, MarketHistory, Types, Liquidity, LogisticsPlanning
from eve_parser.models import models
from datetime import datetime
from eve_parser.include.parser import Parser


def run(*args):
    start = datetime.now()
    calculate_logistics(args)
    print("start at: %s\n end at: %s" % (start, datetime.now()))
    Parser.parser_status("Calculate logistics", "Done \nStart at: %s\n end at: %s" % (start, datetime.now()), 0, 0)


def calculate_logistics(args):
    region_from = args[0]
    region_to = args[1]
    day_turnover_threshold = float(args[2])
    print("Calculate logistics from %s to %s" % (region_from, region_to))
    for item_type in TopTypes.objects.values_list("type_id"):
        Parser.parser_status("Calculate logistics", "item_type", region_to, item_type[0])
        print("Item type: %s" % item_type[0])
        # get data from database
        item_describe = Types.objects.get(type_id=item_type[0])
        try:
            liquidity_from = Liquidity.objects.get(type_id=item_type[0], region_id=region_from)
        except models.ObjectDoesNotExist as e:
            continue
        try:
            liquidity_to = Liquidity.objects.get(type_id=item_type[0], region_id=region_to)
        except models.ObjectDoesNotExist as e:
            continue

        if liquidity_to.day_turnover >= day_turnover_threshold and liquidity_from.day_turnover >= day_turnover_threshold:
            log = list(LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                                        region_id_to=region_to))
            if len(log) < 1:
                logistics_planning = LogisticsPlanning.objects.create(
                    type_id=item_type[0], packaged_volume=item_describe.packaged_volume, region_id_from=region_from, region_id_to=region_to,
                    price_from=liquidity_from.price, price_to=liquidity_to.price, price_diff=liquidity_from.price - liquidity_to.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=(liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume / 1000000,
                    profit_to=(liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume) / 1000000
                logistics_planning.save()
            else:
                logistics_planning = LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                                                      region_id_to=region_to).update(
                    price_from=liquidity_from.price, price_to=liquidity_to.price,
                    price_diff=liquidity_from.price - liquidity_to.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=(liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume / 1000000,
                    profit_to=(liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume / 1000000)






