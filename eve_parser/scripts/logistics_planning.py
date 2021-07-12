from eve_parser.models import TopTypes, Regions, Types, Liquidity, LogisticsPlanning
from eve_parser.models import models
from datetime import datetime
from eve_parser.include.parser import Parser


def run(*args):
    start = datetime.now()
    region_from = [args[0]]
    region_to = [args[1]]
    day_turnover_threshold = float(args[2])
    if region_from[0] == "*":
        region_from = Regions.objects.values_list("region_id")
    if region_to[0] == "*":
        region_to = Regions.objects.values_list("region_id")
    for reg_from in region_from:
        for reg_to in region_to:
            if int(reg_from[0]) < int(reg_to[0]):
                calculate_logistics(reg_from[0], reg_to[0], day_turnover_threshold)
    print("start at: %s\n end at: %s" % (start, datetime.now()))
    Parser.parser_status("Calculate logistics", "Done \nStart at: %s\n end at: %s" % (start, datetime.now()), 0, 0)


def calculate_logistics(region_from, region_to, day_turnover_threshold):
    print("Calculate logistics from %s to %s" % (region_from, region_to))
    parser_write = 0
    for item_type in TopTypes.objects.values_list("type_id"):
        parser_write += 1
        if parser_write == 50:
            Parser.parser_status("Calculate logistics", "From:" + str(region_from), region_to, item_type[0])
            parser_write = 0
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
                    price_from=liquidity_from.price, price_to=liquidity_to.price, price_diff=liquidity_to.price - liquidity_from.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=float((liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume) / 1000000,
                    profit_to=float((liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume) / 1000000)
                logistics_planning.save()
            else:
                logistics_planning = LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                                                      region_id_to=region_to).update(
                    price_from=liquidity_from.price, price_to=liquidity_to.price,
                    price_diff=liquidity_to.price - liquidity_from.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=float((liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume) / 1000000,
                    profit_to=float((liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume) / 1000000)
